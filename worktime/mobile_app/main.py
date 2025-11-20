from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
import sqlite3
from datetime import datetime
from database import Database
import hashlib
import os

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 20
        self.padding = 20
                 # Company Name field
        self.company_name = MDTextField(
            hint_text="Company Name",
            helper_text="Enter your company name",
            helper_text_mode="on_error",
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            size_hint_x=0.8
        )
        self.add_widget(self.company_name)
        # Username field
        self.username = MDTextField(
            hint_text="Username",
            helper_text="Enter your username",
            helper_text_mode="on_error",
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            size_hint_x=0.8
        )
        self.add_widget(self.username)
        # Password field
        self.password = MDTextField(
            hint_text="Password",
            helper_text="Enter your password",
            helper_text_mode="on_error",
            password=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint_x=0.8
        )
        self.add_widget(self.password)
        # Login button
        self.login_button = MDRaisedButton(
            text="Login",
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            on_release=self.validate_login
        )
        self.add_widget(self.login_button)

    def validate_login(self, instance):
        username = self.username.text
        password = self.password.text
        company = self.company_name.text
        app = MDApp.get_running_app()
        # Simulate: dbwr.validate_user_login returns True if user exists and password matches
        # dbwr.validate_new_user returns True if user is new (first login)
        # Validate credentials first
        if not db.validate_user_login(username, password):
            from kivymd.toast import toast
            toast("Invalid username or password")
            return

        # If the user is marked as new, force change-password flow
        if db.validate_new_user(username):
            app.switch_screen('change_password', username, company)
            return

        # Normal login: verify current password and go to main screen
        if db.verify_current_password(username, password):
            app.switch_screen('main', username, company)
        else:
            from kivymd.toast import toast
            toast("Invalid username or password")

class ChangePasswordScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 20
        self.padding = 20
        self.info_label = MDLabel(
            text="Change Password (First Login)",
            halign="center",
            pos_hint={'center_x': 0.5, 'center_y': 0.8},
        )
        self.add_widget(self.info_label)
        self.current_password = MDTextField(
            hint_text="Current Password",
            password=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            size_hint_x=0.8
        )
        self.add_widget(self.current_password)
        self.new_password = MDTextField(
            hint_text="New Password",
            password=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            size_hint_x=0.8
        )
        self.add_widget(self.new_password)
        self.repeat_password = MDTextField(
            hint_text="Repeat New Password",
            password=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint_x=0.8
        )
        self.add_widget(self.repeat_password)
        self.submit_button = MDRaisedButton(
            text="Submit",
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            on_release=self.change_password
        )
        self.add_widget(self.submit_button)

    def change_password(self, instance):
        app = MDApp.get_running_app()
        username = app.username
        current_pw = self.current_password.text
        new_pw = self.new_password.text
        repeat_pw = self.repeat_password.text
        # Validate current password
        if not db.verify_current_password(username, current_pw):
            from kivymd.toast import toast
            toast("Current password is incorrect!")
            return
        # New password must be different
        if current_pw == new_pw:
            from kivymd.toast import toast
            toast("New password cannot be same as old password!")
            return
        # New passwords must match
        if new_pw != repeat_pw:
            from kivymd.toast import toast
            toast("New passwords do not match!")
            return
        # Update password
        if db.update_new_password(username, new_pw):
            from kivymd.toast import toast
            toast("Password changed successfully!")
            app.switch_screen('main', username, app.company)
        else:
            from kivymd.toast import toast
            toast("Failed to change password!")

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 20
        self.padding = 20
        
        # Time display
        self.time_label = MDLabel(
            text="",
            halign="center",
            pos_hint={'center_x': 0.5, 'center_y': 0.8},
        )
        self.add_widget(self.time_label)
        Clock.schedule_interval(self.update_time, 1)
        
        # Login button
        self.login_btn = MDRaisedButton(
            text="Login",
            pos_hint={'center_x': 0.3, 'center_y': 0.6},
            on_release=self.login
        )
        self.add_widget(self.login_btn)
        
        # Logout button
        self.logout_btn = MDRaisedButton(
            text="Logout",
            pos_hint={'center_x': 0.7, 'center_y': 0.6},
            on_release=self.logout
        )
        self.add_widget(self.logout_btn)
        
        # Download button
        self.download_btn = MDRaisedButton(
            text="Download Report",
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            on_release=self.download_report
        )
        self.add_widget(self.download_btn)

    def update_time(self, dt):
        self.time_label.text = datetime.now().strftime("%H:%M:%S")
        
    def login(self, instance):
        app = MDApp.get_running_app()
        username = app.username
        login_time = datetime.now().strftime("%H:%M:%S")
        company = app.company
        if db.save_login(username, company, login_time):
            app.switch_screen('end', username, company)
            from kivymd.toast import toast
            app.custom_toast("Login time was successfully recorded!")   
        else:
            app.switch_screen('end', username, company)
            from kivymd.toast import toast
            app.custom_toast("Failed to record login time!")
        
    def logout(self, instance):
        app = MDApp.get_running_app()
        username = app.username
        logout_time = datetime.now().strftime("%H:%M:%S")
        company = app.company
        if db.save_logout(username, logout_time):
            app.switch_screen('end', username, company)
            from kivymd.toast import toast
            app.custom_toast("Logout time was successfully recorded!")
            #TODO: Show the summary of the work hours for the day and switch to login screen
        else:
            app.switch_screen('end', username, company)
            from kivymd.toast import toast
            app.custom_toast("Failed to record logout time!")
        
    def download_report(self, instance):
        # TODO: Implement report download
        pass

class EndScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 20
        self.padding = 20
        
        # Time display
        self.time_label = MDLabel(
            text="",
            halign="center",
            pos_hint={'center_x': 0.5, 'center_y': 0.8},
        )
        self.add_widget(self.time_label)
        Clock.schedule_interval(self.update_time, 1)

       # OK button
        self.ok_btn = MDRaisedButton(
            text="OK",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            on_release=self.ok
        )
        self.add_widget(self.ok_btn) 


    def update_time(self, dt):
        self.time_label.text = datetime.now().strftime("%H:%M:%S")

    def ok(self, instance):
        #TODO: Switch to login screen and user is logged out
        app = MDApp.get_running_app()
        app.logout()

class WorktimeMobileApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username = ""
        self.company = ""
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        self.sm = MDScreenManager()
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(ChangePasswordScreen(name='change_password'))
        self.sm.add_widget(EndScreen(name='end'))
        return self.sm
    def switch_screen(self, screen_name, username="", company=""):
        self.username = username
        self.company = company
        self.sm.current = screen_name
    def on_start(self):
        self.init_database()

    def logout(self):
        self.username = ""
        self.company = ""
        self.sm.current = 'login'
       
    def custom_toast(self, display_message, font_name="Roboto", font_size=20):
        layout = BoxLayout(size_hint=(None, None), size=(300, 50), pos_hint={"center_x": 0.5, "center_y": 0.1})
        label = Label(text=display_message, font_name=font_name, font_size=font_size, color=(0, 0, 0, 1))
        layout.add_widget(label)
        Window.add_widget(layout)
        Clock.schedule_once(lambda dt: Window.remove_widget(layout), 10)  # Remove after 10 seconds

    def init_database(self):
        conn = sqlite3.connect('worktime.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                company TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS work_hours (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                login_time TEXT,
                logout_time TEXT,
                hours_worked REAL,
                company TEXT,
                date TEXT,
                FOREIGN KEY (employee_id) REFERENCES users (id)
            )
        ''')
        conn.commit()
        conn.close()

if __name__ == '__main__':
    if platform == 'android':
        from android.permissions import request_permissions, Permission
        request_permissions([
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE
        ])
    db=Database()
    db.setup_database()
    Window.size = (400, 600)  # For desktop testing
    WorktimeMobileApp().run()
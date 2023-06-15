import calendar
from datetime import datetime, date
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
import download_timesheet as dt
import PySimpleGUI as sg
import mysql.connector as mysql
import pandas as pd


now = datetime.now()
font = ('Helvetica', 12, 'bold italic')
sg.theme('Green')
sg.set_options(font=font)
color = (sg.theme_background_color(), sg.theme_background_color())
system_date = date.today()

mydb = mysql.connect(
    host="localhost",
    user="admin",
    password="root",
    database="worktime_database",
    auth_plugin='mysql_native_password'
)

my_cursor = mydb.cursor()


def user_database_table_check():
    my_cursor.execute("SHOW TABLES LIKE 'user_database'")
    table_exists = my_cursor.fetchone()

    if not table_exists:
        my_cursor.execute("""
            CREATE TABLE user_database(
                id INTEGER PRIMARY KEY,
                employee_id INTEGER,
                company_name TEXT,
                username TEXT,
                password TEXT
            )
        """)
        mydb.commit()


def validate_user_login(companyname, username, password):
    my_cursor.execute('SELECT * FROM user_database WHERE username = %s AND company_name = %s', (username, companyname,))
    user = my_cursor.fetchone()

    if user and user[4] == password:
        return True
    return False


def database_table_check():
    my_cursor.execute("SHOW TABLES LIKE 'work_hours'")
    table_exists = my_cursor.fetchone()
    # If the table doesn't exist, create it
    if not table_exists:
        my_cursor.execute("""
            CREATE TABLE work_hours (
                date DATE,
                login TIME,
                logout TIME,
                hours FLOAT
            )
        """)
        mydb.commit()


def get_pdf_name():
    # finding current month name
    month = calendar.month_name[now.month]
    return month + "_" + "timesheet.pdf"


def save_login_data(to_login):
    my_cursor.execute("INSERT INTO work_hours (date, login) VALUES (%s, %s) ",
                      (system_date, to_login))
    mydb.commit()


def save_logout_data(to_logout):
    my_cursor.execute("UPDATE work_hours SET logout = %s WHERE date = %s", (to_logout, system_date))
    mydb.commit()


def calculate_hours():
    my_cursor.execute("SELECT login, logout FROM work_hours WHERE date = CURRENT_DATE LIMIT 0, 1")
    result = my_cursor.fetchone()
    to_login = result[0]
    to_logout = result[1]
    # format = '%H:%M'
    no_hours = to_logout - to_login
    stunden = "{:.2f}".format(no_hours.total_seconds() / 3600)
    lunch_break = 0.75
    stunden_with_break = float(stunden) - lunch_break
    my_cursor.execute("UPDATE work_hours SET hours = %s WHERE date = %s", (stunden_with_break, system_date))
    mydb.commit()
    return stunden


def worktime_gui():

    # Define the path to the images
    login_image = 'in.png'
    logout_image = 'out.png'
    download_image =  'download.png'
    # Define the corporate theme for the window
    sg.theme('Green')

    layout = [
        [
            sg.Text('LOGIN', justification='center', font=('Arial', 14, 'bold')),
            sg.Button('', button_color=color, image_filename=login_image, border_width=0, pad=(30, 20), key='login'),
            sg.Text('LOGOUT', justification='center', font=('Arial', 14, 'bold')),
            sg.Button('', button_color=color, image_filename=logout_image, border_width=0, pad=(30, 20), key='logout')
        ],
        [
            sg.Button('', button_color=color, image_filename=download_image, border_width=0, pad=(30, 20), key='download')
        ]
    ]

    # Create the window
    window = sg.Window('WORKTIME GRABBER', layout)
    # Display and interact with the Window using an Event Loop
    while True:
        event, values = window.read()
        # check if table exists in database
        database_table_check()
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED:
            break
        # Output a message to the window
        else:
            if event == 'login':
                login_time = now.strftime("%H:%M:%S")
                save_login_data(login_time)
                if sg.popup_auto_close("LogIN Time {} !!!".format(login_time), button_type=5, auto_close=True,
                                       auto_close_duration=2):
                    break
            elif event == 'logout':
                logout_time = now.strftime("%H:%M:%S")
                save_logout_data(logout_time)
                stunden_pro_tag = calculate_hours()
                if sg.popup_auto_close("LogOUT Time {} !!!.\n".format(logout_time) + "Working hours {}.\n".format(
                        stunden_pro_tag) + "INFO : Default break of 45 mins is deducted !!", button_type=5,
                                       auto_close=True,
                                       auto_close_duration=2):
                    break
            elif event == 'download':
                dt.download_table_to_pdf("work_hours", get_pdf_name(), username, mydb)
                if sg.popup_auto_close("Document Downloaded!!!", button_type=5, auto_close=True, auto_close_duration=2):
                    break

    # Finish up by removing from the screen
    window.close()


# Define the path to the logo image file
logo_path = 'logo.png'

# Create an sg.Image element for the logo
logo = sg.Image(logo_path)

# Define the corporate theme for the window
sg.theme('Green')


layout = [
    [
        sg.Column(
            [
                [logo],
                [sg.Text('You can only manage time if you track it right. - Spica’s team', justification='center',
                       pad=(1, 50))],
                [sg.Text('Company Name', font=('Arial', 14, 'bold'))],
                [sg.Input(key='-COMPANYNAME-', size=(20, 1))],
                [sg.Text('Username', font=('Arial', 14, 'bold'))],
                [sg.Input(key='-USERNAME-', size=(20, 1))],
                [sg.Text('Password', font=('Arial', 14, 'bold'))],
                [sg.Input(key='-PASSWORD-', size=(20, 1), password_char='*')],
                [sg.Button('Login', font=('Arial', 14), size=(10, 1))]
            ],
            element_justification='c',
        )
    ]
]

window = sg.Window('Login', layout, element_justification='c')

while True:
    event, values = window.read()
    user_database_table_check()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Login':
        companyname = values['-COMPANYNAME-']
        username = values['-USERNAME-']
        password = values['-PASSWORD-']
        if validate_user_login(companyname, username, password):
            window.close()
            worktime_gui()
        else:
            sg.popup('Invalid username or password')

window.close()

from datetime import datetime
import download_timesheet as dt
import PySimpleGUI as sg
import database_read_write as dbwr
from database import Worktimedb
import worktime_helper as wh

now = datetime.now()
font = ('Helvetica', 12, 'bold italic')
sg.theme('Green')
sg.set_options(font=font)
color = (sg.theme_background_color(), sg.theme_background_color())
wt = Worktimedb()


def worktime_gui():
    # Define the path to the images
    login_image = 'in.png'
    logout_image = 'out.png'
    download_image = 'download.png'
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
            sg.Button('', button_color=color, image_filename=download_image, border_width=0, pad=(30, 20),
                      key='download')
        ]
    ]

    # Create the window
    window = sg.Window('WORKTIME GRABBER', layout)
    # Display and interact with the Window using an Event Loop
    while True:
        event, values = window.read()
        # check if table exists in database
        dbwr.database_table_check()
        employee_id = dbwr.get_employee_id(username)
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED:
            break
        # Output a message to the window
        else:
            if event == 'login':
                login_time = now.strftime("%H:%M:%S")
                dbwr.save_login_data(login_time, employee_id, companyname)
                if sg.popup_auto_close("LogIN Time {} !!!".format(login_time), button_type=5, auto_close=True,
                                       auto_close_duration=2):
                    break
            elif event == 'logout':
                logout_time = now.strftime("%H:%M:%S")
                dbwr.save_logout_data(logout_time, employee_id)
                stunden_pro_tag = dbwr.calculate_hours(employee_id)
                if sg.popup_auto_close("LogOUT Time {} !!!.\n".format(logout_time) + "Working hours {}.\n".format(
                        stunden_pro_tag) + "INFO : Default break of 45 mins is deducted !!", button_type=5,
                                       auto_close=True,
                                       auto_close_duration=2):
                    break
            elif event == 'download':
                dt.download_table_to_pdf("work_hours", wh.get_pdf_name(), username, employee_id, wt.connect())
                if sg.popup_auto_close("Document Downloaded!!!", button_type=5, auto_close=True, auto_close_duration=2):
                    break

    # Finish up by removing from the screen
    window.close()


def popup_gui(message):
    # Create a layout for the pop-up message
    layout = [
        [sg.Text(message)],
        [sg.Button("OK")]
    ]

    # Create the pop-up window
    window = sg.Window("Info", layout)

    # Event loop for the pop-up window
    while True:
        event, values = window.read()
        if event == "OK" or event == sg.WINDOW_CLOSED:
            break

    # Close the pop-up window
    window.close()


def change_password_gui(username):
    while True:
        layout = [
            [
                sg.Column(
                    [
                        [sg.Text('Please change the password !!', justification='center',
                                 pad=(1, 50))],
                        [sg.Text('Current Password', font=('Arial', 14, 'bold'))],
                        [sg.Input(key='-CURRENTPASSWORD-', size=(20, 1), password_char='*')],
                        [sg.Text('New Password', font=('Arial', 14, 'bold'))],
                        [sg.Input(key='-NEWPASSWORD-', size=(20, 1), password_char='*')],
                        [sg.Text('Repeat New Password', font=('Arial', 14, 'bold'))],
                        [sg.Input(key='-REPEATPASSWORD-', size=(20, 1), password_char='*')],
                        [sg.Button('Submit', font=('Arial', 14), size=(10, 1))]
                    ],
                    element_justification='c',
                )
            ]
        ]

        window = sg.Window('Change Password', layout, element_justification='c')

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                break
            if event == 'Submit':
                current_password = values['-CURRENTPASSWORD-']
                new_password = values['-NEWPASSWORD-']
                repeat_password = values['-REPEATPASSWORD-']
                # todo write function to check current password
                if wh.verify_password_match(new_password, repeat_password):
                    if dbwr.update_new_password(username, new_password):
                        popup_gui("Password changed successfully !!")
                        window.close()
                        return
                else:
                    popup_gui("passwords do not match !!")
                    window.close()
                    break


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
    dbwr.user_database_table_check()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Login':
        companyname = values['-COMPANYNAME-']
        username = values['-USERNAME-']
        password = values['-PASSWORD-']
        if dbwr.validate_user_login(username, password):
            window.close()
            worktime_gui()
        else:
            if dbwr.validate_new_user(username):
                window.close()
                change_password_gui(username)
                worktime_gui()
            else:
                sg.popup('Invalid username or password')

window.close()

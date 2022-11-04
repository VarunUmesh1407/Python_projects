from datetime import datetime, date
import pandas as pd
import PySimpleGUI as sg
import os

now = datetime.now()
font = ('Helvetica', 12, 'bold italic')
sg.theme('Dark')
sg.set_options(font=font)
colors = (sg.theme_background_color(), sg.theme_background_color())


def save_login_data(login):
    todate = date.today()
    details_dict = {"Date": [todate], "Clock IN": [login]}
    rows_to_add = pd.DataFrame(details_dict)
    if os.path.exists('Timesheet.csv'):
        df = pd.read_csv('Timesheet.csv')
        df = pd.concat([df, rows_to_add])
        df.to_csv('Timesheet.csv', mode='w+', index=False, header=True)
    else:
        rows_to_add.to_csv('Timesheet.csv', mode='w+', index=False, header=True)


def save_logout_data(logout):
    todate = date.today()
    logout_dict = {"Clock OUT": [logout]}
    cols_to_add = pd.DataFrame(logout_dict)
    if os.path.exists('Timesheet.csv'):
        df = pd.read_csv('Timesheet.csv')
        df = df.merge(cols_to_add, left_index=True, right_index=True)
        df.to_csv('Timesheet.csv', mode='w+', index=False, header=True)
    else:
        print("ERROR saving Time")


layout = [[sg.Text("Time Stamp Grab")],
          [sg.Button('Login', button_color=colors, image_filename="g.png", border_width=0)],
          [sg.Output(size=(40, 2), key='-login-')],
          [sg.Button('Logout', button_color=colors, image_filename="r.png", border_width=0)],
          [sg.Output(size=(40, 2), key='-logout-')]]

# Create the window
window = sg.Window('WORKTIME GRABBER', layout, finalize=True)
# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    # Output a message to the window
    else:
        if event == 'Login':
            login_time = now.strftime("%H:%M")
            window['-login-'].update(login_time)
            save_login_data(login_time)
        elif event == 'Logout':
            logout_time = now.strftime("%H:%M:%S")
            window['-logout-'].update(logout_time)
            #save_logout_data(logout_time)
# Finish up by removing from the screen
window.close()

import os
import pandas as pd
import random
import PySimpleGUI as sg

# Define the window's contents
layout = [[sg.Text("Website name/link with new login")],
          [sg.Input(key='-webIN-')],
          [sg.Text("Email ID used for login")],
          [sg.Input(key='-mailIN-')],
          [sg.Text("Length of the required password")],
          [sg.Input(key='-lenIN-')],
          [sg.Output(size=(40, 2), key='-lenOUT-')],
          [sg.Button('Ok', button_color="green"), sg.Button('Quit', button_color="red")]]

# Create the window
window = sg.Window('PASSWORD GENERATOR', layout)


# save the password data in a csv file to access later
def save_password_details(website_id, email_address, password):
    details_dict = {"WEB_ID": [website_id], "EMAIL_ID": [email_address], "PASSWORD": [password]}
    rows_to_add = pd.DataFrame(details_dict)
    if os.path.exists('Password_details.csv'):
        df = pd.read_csv('Password_details.csv')
        df = pd.concat([df, rows_to_add])
        df.to_csv('Password_details.csv', mode='w+', index=False, header=True)
    else:
        rows_to_add.to_csv('Password_details.csv', mode='w+', index=False, header=True)


# generate random passwords
def generate_passwords(length_of_passwords):
    ran_characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVXYZ!@§$&*().,0123456789'
    passwords = ''
    for i in range(length_of_passwords):
        passwords += random.choice(ran_characters)
    return passwords


# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    # Output a message to the window
    else:
        web_id = values['-webIN-']
        email_id = values['-mailIN-']
        password_length = values['-lenIN-']
        output_passwords = generate_passwords(int(password_length))
        window['-lenOUT-'].update(output_passwords)
        save_password_details(web_id, email_id, output_passwords)

# Finish up by removing from the screen
window.close()

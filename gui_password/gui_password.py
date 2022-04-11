import random
import PySimpleGUI as sg

# Define the window's contents
layout = [[sg.Text("Length of the required password")],
          [sg.Input(key='-lenIN-')],
          [sg.Multiline(size=(40, 2), key='-lenOUT-')],
          [sg.Button('Ok'), sg.Button('Quit')]]

# Create the window
window = sg.Window('PASSWORD GENERATOR', layout)


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
        val2 = values['-lenIN-']
        output_passwords = generate_passwords(int(val2))
        window['-lenOUT-'].update(output_passwords)

# Finish up by removing from the screen
window.close()

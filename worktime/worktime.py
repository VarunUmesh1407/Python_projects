from datetime import datetime, date
import mysql.connector
import PySimpleGUI as sg
import calendar
import pandas as pd
import pdfkit

now = datetime.now()
font = ('Helvetica', 12, 'bold italic')
sg.theme('Dark')
sg.set_options(font=font)
colors = (sg.theme_background_color(), sg.theme_background_color())
system_date = date.today()


mydb = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="root",
    database="worktime_database"
)

my_cursor = mydb.cursor()

def get_pdf_name():
      #finding current month name
      month =  calendar.month_name[now.month]
      return (month + "_" + "timesheet.pdf")

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
    #format = '%H:%M'
    no_hours = to_logout - to_login
    stunden = "{:.2f}".format(no_hours.total_seconds() / 3600)
    lunch_break = 0.75
    stunden_with_break = float(stunden) - lunch_break
    my_cursor.execute("UPDATE work_hours SET hours = %s WHERE date = %s", (stunden_with_break, system_date))
    mydb.commit()
    return stunden


def download_table_to_pdf(table_name, pdf_file):

    # Read the table into a DataFrame
    df = pd.read_sql_query("SELECT * FROM " + table_name, mydb)
    # Close the connection
    mydb.close()

    # convert DataFrame to html
    html = df.to_html()
    # write to file
    with open("table.html", "w") as f:
         f.write(html)

    pdfkit.from_file("table.html", pdf_file)


layout = [[sg.Text("LOGIN", justification="center"),
          sg.Button(' ', button_color=colors, image_filename="in.png", border_width=0, pad=(40,1), key="login"),
          sg.Text("LOGOUT",justification="center"),
          sg.Button(' ', button_color=colors, image_filename="out.png", border_width=0,pad=(50,1), key="logout")],
          [sg.Text('You can only manage time if you track it right. - Spica’s team', justification='center', pad=(1, 50))],
          [sg.Button(' ',button_color=colors, image_filename="download.png",key='download' )]]

# Create the window
window = sg.Window('WORKTIME GRABBER', layout, background_color='#3a3f44', finalize=True, size=(530, 320))
# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED:
        break
    # Output a message to the window
    else:
        if event == 'login':
            login_time = now.strftime("%H:%M:%S")
            save_login_data(login_time)
            if sg.popup_auto_close("LogIN Time {} !!!".format(login_time), button_type=5, auto_close=True, auto_close_duration=2):
                break
        elif event == 'logout':
            logout_time = now.strftime("%H:%M:%S")
            save_logout_data(logout_time)
            stunden_pro_tag = calculate_hours()
            if sg.popup_auto_close("LogOUT Time {} !!!.\n".format(logout_time) + "Working hours {}.\n".format(stunden_pro_tag) + "INFO : Default break of 45mins is deducted !!" , button_type=5, auto_close=True, auto_close_duration=2):
                break
        elif event == 'download':
            download_table_to_pdf("work_hours", get_pdf_name())
            if sg.popup_auto_close("Document Downloaded!!!" , button_type=5, auto_close=True, auto_close_duration=2):
                break

# Finish up by removing from the screen
window.close()

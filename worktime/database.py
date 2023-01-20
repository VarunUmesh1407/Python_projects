import mysql.connector
import datetime

mydb = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="root",
    database="worktime_database"
)

mycursor = mydb.cursor()


# mycursor.execute("CREATE TABLE work_hours (id INT AUTO_INCREMENT PRIMARY KEY, date DATE NOT NULL, login TIME NOT NULL, logout TIME NOT NULL, hours INT NOT NULL)")

def update_timsheet_table(todate, tologin):
    mycursor.execute("INSERT INTO work_hours (date, login) VALUES (%s, %s)", (todate, tologin))
    mydb.commit()


def update_logout_time(tologout):
    current_date = datetime.datetime.now().date()
    mycursor.execute("UPDATE work_hours SET logout = %s WHERE date = %s" , (tologout, current_date))
    mydb.commit()


def calculate_hours():
    login_details = mycursor.execute("SELECT login, logout FROM work_hours WHERE date = CURRENT_DATE")
    result = mycursor.fetchone()
    tologin = result[0]
    tologout = result[1]
    format = '%H:%M'
    no_hours = tologout - tologin
    stunden = no_hours.total_seconds() / 3600
    lunch_break = 0.75
    stunden_without_break = stunden - lunch_break
    print(stunden)
    current_date = datetime.datetime.now().date()
    mycursor.execute("UPDATE work_hours SET hours = %s WHERE date = %s", (stunden, current_date))
    print("added no. of hours")
    mydb.commit()


#update_timsheet_table("2022-12-27", "09:00:00")
#update_logout_time("18:00:00")
calculate_hours()

from database import Worktimedb
from datetime import date

wt = Worktimedb()
wt.connect()
system_date = date.today()


def user_database_table_check():
    table_check_query = "SHOW TABLES LIKE 'user_database'"
    create_table_query = """
               CREATE TABLE user_database(
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   employee_id INTEGER,
                   company_name TEXT,
                   username TEXT,
                   password TEXT
               )
           """
    table_exists = wt.execute_query(table_check_query)

    if not table_exists:
        wt.execute_query(create_table_query)
        wt.commit()


def validate_user_login(username, password):
    user_query = 'SELECT * FROM user_database WHERE username = %s'
    parameters = (username,)
    user = wt.execute_query(user_query, parameters)

    if user and user[4] == password:
        return True
    return False


def get_employee_id(username):
    user_query = 'SELECT * FROM user_database WHERE username = %s'
    parameters = (username,)
    user = wt.execute_query(user_query, parameters)

    return user[1]


def database_table_check():
    table_check_query = "SHOW TABLES LIKE 'work_hours'"
    create_table_query = """
            CREATE TABLE work_hours (
                id INT AUTO_INCREMENT PRIMARY KEY,
                employee_id INTEGER,
                date DATE,
                login TIME,
                logout TIME,
                hours FLOAT
            )
        """
    table_exists = wt.execute_query(table_check_query)
    # If the table doesn't exist, create it
    if not table_exists:
        wt.execute_query(create_table_query)
        wt.commit()


def save_login_data(to_login, employee_id, companyname):
    insert_login_query = "INSERT INTO work_hours (employee_id, company_name, date, login) VALUES (%s, %s,%s, %s) "
    parameters = (employee_id, companyname, system_date, to_login)
    wt.execute_query(insert_login_query, parameters)
    wt.commit()


def save_logout_data(to_logout, employee_id):
    update_logout_query = "UPDATE work_hours SET logout = %s WHERE date = %s  AND employee_id = %s"
    parameters = (to_logout, system_date, employee_id)
    wt.execute_query(update_logout_query, parameters)
    wt.commit()


def calculate_hours(employee_id):
    get_data_query = "SELECT login, logout FROM work_hours WHERE date = CURRENT_DATE AND employee_id = %s LIMIT 0, 1"
    parameters_data = (employee_id, )
    update_hours = "UPDATE work_hours SET hours = %s WHERE date = %s and employee_id = %s"

    result = wt.execute_query(get_data_query, parameters_data)
    to_login = result[0]
    to_logout = result[1]
    # format = '%H:%M'
    no_hours = to_logout - to_login
    stunden = "{:.2f}".format(no_hours.total_seconds() / 3600)
    lunch_break = 0.75
    stunden_with_break = float(stunden) - lunch_break
    parameters_hours = (stunden_with_break, system_date, employee_id)
    wt.execute_query(update_hours, parameters_hours)
    wt.commit()
    return stunden_with_break

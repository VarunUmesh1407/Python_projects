import calendar
from datetime import datetime

now = datetime.now()


def get_pdf_name():
    # finding current month name
    month = calendar.month_name[now.month]
    return month + "_" + "timesheet.pdf"


def verify_password_match(new_password, repeat_password):
    # check if the new password entered are same
    if new_password == repeat_password:
        return True
    return False

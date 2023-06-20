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


def verify_new_and_current_password(current_password, new_password):
    # check if current password and new password are same
    if current_password != new_password:
        return True
    return False

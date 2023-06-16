import calendar
from datetime import datetime

now = datetime.now()

def get_pdf_name():
    # finding current month name
    month = calendar.month_name[now.month]
    return month + "_" + "timesheet.pdf"

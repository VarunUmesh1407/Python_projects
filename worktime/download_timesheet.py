# canvas_form.py
import calendar
from datetime import datetime, date

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

now = datetime.now()
month =  "WorkTime of" +  " " + calendar.month_name[now.month]
system_date = date.today().strftime('%Y/%m/%d')




def form(path):
    my_canvas = canvas.Canvas(path, pagesize=letter)
    my_canvas.drawImage("logo.png", 30, 740, width=50, height=30)
    my_canvas.setLineWidth(.3)
    my_canvas.setFont('Helvetica', 16)
    my_canvas.drawString(200, 750, month )
    my_canvas.setFont('Helvetica', 8)
    my_canvas.drawString(500, 750, system_date)
    my_canvas.setFont('Helvetica', 12)
    my_canvas.drawString(30, 703, 'Employee name:')
    my_canvas.drawString(150, 703, "Varun Umesh")
    doc = SimpleDocTemplate(
        "simple_table_with_style.pdf",
        pagesize=letter,
    )
    flowables = []
    data = [
        ['col_{}'.format(x) for x in range(1, 6)],
        [str(x) for x in range(1, 6)],
        ['a', 'b', 'c', 'd', 'e'],
    ]
    tblstyle = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.red),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.blue),
    ])
    tbl = Table(data)
    tbl.setStyle(tblstyle)
    flowables.append(tbl)
    doc.build(flowables)

    my_canvas.save()
if __name__ == '__main__':
    form('canvas_form.pdf')
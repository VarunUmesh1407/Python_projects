import calendar
from datetime import datetime, date

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.lib.units import inch
from reportlab.platypus import PageTemplate, Frame
import pandas as pd

now = datetime.now()
month = "WorkTime of" + " " + calendar.month_name[now.month]
system_date = date.today().strftime('%Y/%m/%d')


def download_table_to_pdf(table_name, pdf_file, username, mydb):
    # Read the table into a DataFrame (assuming you have a valid connection named 'mydb')
    df = pd.read_sql_query("SELECT * FROM " + table_name, mydb)
    df_user = pd.read_sql_query("SELECT * FROM user_database", mydb)

    # Convert DataFrame to table data
    data = [df.columns.tolist()] + df.values.tolist()

    # Generate PDF using reportlab
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)

    # Define styles for the title and date
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name='TitleStyle',
        parent=styles['Title'],
        fontSize=20,
        textColor=colors.black,
        spaceAfter=0.5 * inch,
    )
    date_style = ParagraphStyle(
        name='DateStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.gray,
        spaceAfter=0.2 * inch,
    )

    user_style = ParagraphStyle(
        name='UserStyle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.black,
        spaceAfter=0.5 * inch,
    )

    table_content_style = ParagraphStyle(
        name='TableContentStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        spaceAfter=0.5 * inch,
    )
    # Define the title
    title_name = calendar.month_name[now.month] + " " + "Timesheet"
    title = Paragraph(title_name, title_style)

    # Get today's date
    today = date.today().strftime("%B %d, %Y")
    date_text = f"Date: {today}"
    date_paragraph = Paragraph(date_text, date_style)

    # define general info
    table_content = "This is a time sheet for the month of " + title_name + "."
    content_paragraph = Paragraph(table_content, table_content_style)

    # get user info from database

    # Define table style
    tblstyle = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Table content alignment
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Header font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header bottom padding
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Table content background color
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Table grid lines
    ])

    # Create the table
    table = Table(data)
    table.setStyle(tblstyle)

    # Add logo
    logo = "logo.png"  # Path to your logo image file
    image = Image(logo, width=100, height=50)
    image.hAlign = 'LEFT'

    # Build the PDF document
    elements = [
        image, title,  # Logo and title in the same row
        date_paragraph,  # Date in a separate row
        content_paragraph,  # Info about the document
        table  # Table in a separate row
    ]

    def add_page_borders(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.black)
        canvas.rect(0, 0, doc.pagesize[0], doc.pagesize[1])
        canvas.restoreState()

    doc.build(elements, onFirstPage=add_page_borders, onLaterPages=add_page_borders)

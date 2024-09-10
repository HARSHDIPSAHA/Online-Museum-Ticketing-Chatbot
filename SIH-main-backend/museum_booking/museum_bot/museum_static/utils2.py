import os
import requests
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem, Image
import boto3

def fetch_image(logo_path):
    """Retrieve image from local path or URL."""
    try:
        if os.path.exists(logo_path):  # Check if the image exists locally
            return Image(logo_path, 2*inch, 2*inch)
        else:
            # Assume logo_path is a URL and download the image
            response = requests.get(logo_path)
            if response.status_code == 200:
                image = BytesIO(response.content)
                return Image(image, 2*inch, 2*inch)
            else:
                raise ValueError("Failed to retrieve image from URL.")
    except Exception as e:
        print(f"Error fetching image: {e}")
        return None

def upload_pdf_to_s3(pdf_file_path, pdf_file_name, expiration=120):
    """Upload PDF to S3 and generate a presigned URL."""
    s3 = boto3.client('s3', 
                      aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), 
                      aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'), 
                      region_name='eu-north-1')

    bucket_name = 'sangreh-bot2'
    s3_file_key = f"tickets/{pdf_file_name}"

    s3.upload_file(pdf_file_path, bucket_name, s3_file_key)
    
    presigned_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': s3_file_key},
        ExpiresIn=expiration
    )
    
    return presigned_url

def generate_ticket_pdf(museum_name, num_adults, num_children, date_time, file_name="enjoy_your_trip.pdf", logo_path=None):
    """Generate a PDF ticket."""
    pdf = SimpleDocTemplate(
        file_name, pagesize=A4,
        rightMargin=inch, leftMargin=inch,
        topMargin=inch, bottomMargin=inch
    )

    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    instruction_style = ParagraphStyle('Instructions', fontSize=10, leading=12, spaceBefore=20)

    # Dynamically retrieve the logo
    logo = fetch_image(logo_path)
    if logo:
        logo.hAlign = 'CENTER'

    title = Paragraph(f"<b>{museum_name}</b>", title_style)
    date_time_para = Paragraph(f"Date and Time: {date_time}", normal_style)

    details = [
        ['Number of Adults:', str(num_adults)],
        ['Number of Children:', str(num_children)],
    ]
    table = Table(details)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    instruction_bullets = ListFlowable(
        [
            ListItem(Paragraph("Ticket is valid only for one-time use.", instruction_style)),
            ListItem(Paragraph("All adults and children must be present together at the entrance.", instruction_style)),
            ListItem(Paragraph("Please carry a valid ID along with the ticket for verification.", instruction_style)),
            ListItem(Paragraph("No re-entry is allowed once you exit the museum premises.", instruction_style)),
            ListItem(Paragraph("Keep this ticket with you at all times while inside the museum.", instruction_style)),
        ],
        bulletType='bullet', start='circle'
    )

    elements = [
        logo, Spacer(1, 0.5*inch),
        title, Spacer(1, 0.5*inch),
        date_time_para, Spacer(1, 0.5*inch),
        table, Spacer(1, 0.5*inch),
        instruction_bullets
    ]

    pdf.build(elements)

def generate_ticket_and_upload_to_s3(museum_name, num_adults, num_children, date_time, logo_url, pdf_file_name="ticket.pdf"):
    """Wrapper function to generate a ticket and upload it to S3."""
    generate_ticket_pdf(museum_name, num_adults, num_children, date_time, pdf_file_name, logo_url)
    pdf_url = upload_pdf_to_s3(pdf_file_name, pdf_file_name)
    return pdf_url


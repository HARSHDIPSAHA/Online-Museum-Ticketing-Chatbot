from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem, Image
import boto3
image_path = r"C:\Users\Anshuman Raj\OneDrive\Desktop\SIH main back\SIH-main-backend\museum_booking\museum_bot\museum_static\logo.png"

def upload_pdf_to_s3(pdf_file_path, pdf_file_name, expiration=60):  # Set expiration to 120 seconds (2 minutes)
    s3 = boto3.client('s3', 
                      aws_access_key_id='AKIA2ZIOM5LVAIBZ7BOS', 
                      aws_secret_access_key='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', 
                      region_name='eu-north-1')  # Correct region

    bucket_name = 'sangreh-bot2'
    s3_file_key = f"tickets/{pdf_file_name}"
    
    # Upload the file to S3 (no ACL needed)
    s3.upload_file(pdf_file_path, bucket_name, s3_file_key)
    
    # Generate a pre-signed URL that expires after 120 seconds (2 minutes)
    presigned_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': s3_file_key},
        ExpiresIn=expiration  # Expires in 120 seconds
    )
    
    return presigned_url

def generate_ticket_pdf(museum_name, num_adults, num_children, date_time, file_name="enjoy_your_trip.pdf", logo_path="logo.png"):
    pdf = SimpleDocTemplate(
        file_name, pagesize=A4,
        rightMargin=inch, leftMargin=inch,
        topMargin=inch, bottomMargin=inch
    )

    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    instruction_style = ParagraphStyle(
        'Instructions', fontSize=10, leading=12, spaceBefore=20
    )

    # Load and center the logo at the top
    logo = Image(logo_path, 2*inch, 2*inch)  # Adjust the size as needed
    logo.hAlign = 'CENTER'  # Center align the logo

    title = Paragraph(f"<b>{museum_name}</b>", title_style)

    # Date and time
    date_time = Paragraph(f"Date and Time: {date_time}", normal_style)

    # Ticket details (Number of adults and children)
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

    # Instructions in bullet point format
    instruction_bullets = ListFlowable(
        [
            ListItem(Paragraph("Ticket is valid only for one-time use.", instruction_style)),
            ListItem(Paragraph("All adults and children must be present together at the entrance.", instruction_style)),
            ListItem(Paragraph("Please carry a valid ID along with the ticket for verification.", instruction_style)),
            ListItem(Paragraph("No re-entry is allowed once you exit the museum premises.", instruction_style)),
            ListItem(Paragraph("Keep this ticket with you at all times while inside the museum.", instruction_style)),
        ],
        bulletType='bullet',
        start='circle'
    )

    # Build the document
    elements = [
        logo,  # Align the logo at the top center
        Spacer(1, 0.5*inch),
        title,
        Spacer(1, 0.5*inch),
        date_time,
        Spacer(1, 0.5*inch),
        table,
        Spacer(1, 0.5*inch),
        instruction_bullets
    ]
    
    pdf.build(elements)

# Call the function with your updated file and logo path
museum_name = "NSC, Mumbai"
num_adults = 3
num_children = 4
date_time = "Sunday, 23 February 2025, 02:00 PM"
file_name = "updated_ticket.pdf"
logo_path = image_path  # Specify your logo path
# logo_path = "logo.png"  # Specify your logo path

generate_ticket_pdf(museum_name, num_adults, num_children, date_time, file_name, logo_path)
pdf_url = upload_pdf_to_s3(file_name, file_name, expiration=60)

# Step 3: Print the URL or send it via chatbot
print(f"One-time PDF Link (expires in 1 minutes): {pdf_url}")
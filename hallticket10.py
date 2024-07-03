from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import qrcode
from PIL import Image

def generate_qr_code(data, file_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)
    print("QR code generated successfully!")

def generate_hall_ticket(student_name, exam_date, roll_number, subjects, logo_path, photo_path, output_file):
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter

    # Add college information
    c.setFont("Helvetica-Bold", 12)
    college_info = "MATURI VENKATA SUBBARAO ENGINEERING COLLEGE, NADERGUL, HYD."
    college_info_width = c.stringWidth(college_info, "Helvetica-Bold", 16)
    c.drawString((width - college_info_width) / 2, height - 20, college_info)

    # Add hall ticket title
    c.setFont("Helvetica-Bold", 16)
    hall_ticket_text = "HALL TICKET"
    hall_ticket_text_width = c.stringWidth(hall_ticket_text, "Helvetica-Bold", 16)
    c.drawString((width - hall_ticket_text_width) / 2, height - 50, hall_ticket_text)

    # Student information section
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 70, f"Student Name: {student_name}")
    c.drawString(100, height - 90, f"Exam Date: {exam_date}")
    c.drawString(100, height - 110, f"Roll Number: {roll_number}")
    c.drawString(100, height - 130, "Semester: SEM-1")
    c.drawString(100, height - 150, "Branch: Information Technology")

    # Prepare table data
    table_data = [["Subject", "Date", "Time", "Invigilator's Signature"]]
    for subject, (date, time) in subjects.items():
        table_data.append([subject, date, time, ""])

    # Create the table
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.skyblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Get table dimensions and draw it
    table_width, table_height = table.wrap(width, height)
    table.drawOn(c, 100, height - 250 - table_height)

    # Generate QR code with all information
    qr_code_data = f"Name: {student_name}\nExam Date: {exam_date}\nRoll Number: {roll_number}\nSemester: SEM-1\nBranch: Information Technology\n"
    for subject, (date, time) in subjects.items():
        qr_code_data += f"{subject}: {date}, {time}\n"

    # Generate QR code and place it on the ticket
    qr_code_path = "qrcode.png"
    generate_qr_code(qr_code_data, qr_code_path)
    qr_code_image = ImageReader(qr_code_path)
    c.drawImage(qr_code_image, 100, height - 450 - table_height, width=200, height=200)

    # Draw the photo affixation block
    photo_block_x = width - 220
    photo_block_y = height - 195
    photo_block_width = 70
    photo_block_height = 90
    c.rect(photo_block_x, photo_block_y, photo_block_width, photo_block_height)
    c.setFont("Helvetica", 10)
    c.drawString(photo_block_x, photo_block_y - 10, "Affix Photo Here")

    # Load and draw the student's photo
    try:
        img = Image.open(photo_path)
        img_width, img_height = img.size
        if img_width > photo_block_width or img_height > photo_block_height:
            img.thumbnail((photo_block_width, photo_block_height), Image.ANTIALIAS)
        c.drawImage(img, photo_block_x + (photo_block_width - img_width) / 2, photo_block_y + (photo_block_height - img_height) / 2, width=img_width, height=img_height)
    except Exception as e:
        print(f"Error loading photo: {e}")

    # Load and draw the college logo
    try:
        img = Image.open(logo_path)
        img.verify()
        img = ImageReader(logo_path)
        c.drawImage(img, width - 150, height - 150, width=150, height=150)
    except Exception as e:
        print(f"Error loading logo: {e}")

    # Add the signature of the HOD 
    c.setFont("Helvetica-Bold", 12)
    c.drawString(width - 200, 30, "Signature of the HOD")

    c.save()
    print(f"Hall ticket generated for {student_name} successfully!")

if __name__ == "__main__":
    student_name = input("Enter student name: ")
    roll_number = input("Enter roll number: ") 
    exam_date = "22-07-2024"
    subjects = {
        "Mathematics-I": ("22-07-2024", "02:00 PM - 05:00 PM"),
        "Programming & Problem Solving using C": ("24-07-2024", "02:00 PM - 05:00 PM"),
        "Chemistry": ("26-07-2024", "02:00 PM - 05:00 PM"),
        "English": ("29-07-2024", "02:00 PM - 05:00 PM"),
        "English Lab": ("08-07-2024", "10:00 AM - 12:00 PM"),
        "Chemistry Lab": ("10-07-2024", "10:00 AM - 12:00 PM"),
        "Programming & Problem Solving using C Lab": ("12-07-2024", "10:00 AM - 12:00 PM")
    }
    logo_path = r"C:\Users\Dhanush\Downloads\images.jpeg"
    photo_path = r"path_to_student_photo.jpg" 

    output_file = f"hall_ticket_{roll_number}.pdf" 
    generate_hall_ticket(student_name, exam_date, roll_number, subjects, logo_path, photo_path, output_file)

import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name=f'qr_{data}.png')

def generate_ticket_pdf(ticket):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, f"ZOO FARI - TICKET")
    p.drawString(100, 730, f"Ticket ID: {ticket.ticket_id}")
    p.drawString(100, 710, f"Customer: {ticket.booking.full_name}")
    p.drawString(100, 690, f"Visit Date: {ticket.booking.visit_date}")
    if ticket.booking.selected_package:
        p.drawString(100, 670, f"Package: {ticket.booking.selected_package.package_name}")
    elif ticket.booking.selected_ticket:
        p.drawString(100, 670, f"Ticket Type: {ticket.booking.selected_ticket.name}")
    p.drawString(100, 650, f"Members: {ticket.booking.number_of_members}")
    p.drawString(100, 630, f"Status: {ticket.status}")
    
    p.showPage()
    p.save()
    return buffer.getvalue()

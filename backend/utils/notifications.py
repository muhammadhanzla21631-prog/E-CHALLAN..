import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
try:
    from twilio.rest import Client
except ImportError:
    Client = None

# Configuration (Best practice: Load from Environment Variables)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("MAIL_SENDER", "your-email@gmail.com")
SENDER_PASSWORD = os.getenv("MAIL_PASSWORD", "your-app-password")

TWILIO_SID = os.getenv("TWILIO_SID", "your_twilio_sid")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN", "your_twilio_token")
TWILIO_FROM = os.getenv("TWILIO_FROM", "whatsapp:+14155238886")

def send_email_notification(to_email: str, subject: str, body: str):
    """Sends an email notification via Gmail."""
    if not to_email:
        print("Error: No recipient email provided.")
        return False

    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Connect to server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, to_email, text)
        server.quit()
        print(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def send_whatsapp_notification(to_number: str, body: str):
    """Sends a WhatsApp notification via Twilio."""
    if not Client:
        print("Twilio library not installed.")
        return False
        
    if not to_number:
        print("Error: No recipient number provided.")
        return False

    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        
        # Ensure number is in correct format (e.g., whatsapp:+923001234567)
        if not to_number.startswith("whatsapp:"):
            to_number = f"whatsapp:{to_number}"
            
        message = client.messages.create(
            from_=TWILIO_FROM,
            body=body,
            to=to_number
        )
        print(f"WhatsApp message sent: {message.sid}")
        return True
    except Exception as e:
        print(f"Failed to send WhatsApp: {e}")
        return False

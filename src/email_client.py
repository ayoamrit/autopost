# Sends a daily email containing the generated quote image and caption.
# Uses the smtplib library.

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv
from logger import get_logger

load_dotenv()
log = get_logger(__name__)

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

# SMTP server settings for Gmail
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


# Function to send an email with the quote image and caption:
# - Body: the caption and hashtags
# - Attachment: the generated quote image
def send_email(image_path: str, caption: dict, remaining_count: int) -> bool:
    
    if not os.path.exists(image_path):
        log.error("Error: image file not found at %s", image_path)
        return False
    
    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD:
        log.error("Error: EMAIL_ADDRESS and EMAIL_APP_PASSWORD must be set in the .env file.")
        return False
    
    # Determine the reminder message based on the remaining quote count
    if remaining_count == 0:
        reminder = "No more quotes left! Please add more quotes to the database."
    elif remaining_count <= 5:
        reminder = f"Only {remaining_count} quotes left! Consider adding more quotes to the database soon."
    else:
        reminder = f"{remaining_count} quotes remaining in the database."
    
    try:
        # Build the email message
        message = MIMEMultipart()
        message["From"] = EMAIL_ADDRESS
        message["To"] = EMAIL_ADDRESS # Sending to self
        message["Subject"] = "Daily Quote"
        
        # Email body with caption and hashtags
        body = (
            f"CAPTION:\n{caption['caption']}\n\n"
            f"HASHTAGS:\n{caption['hashtags']}\n\n"
            f"Database: {reminder}\n"
        )
        message.attach(MIMEText(body, "plain"))
        
        # Attach the quote image
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            image_attachment = MIMEImage(image_data, name=os.path.basename(image_path))
            message.attach(image_attachment)
            
        # Connect to the SMTP server and send the email
        log.info("Sending email to %s...", EMAIL_ADDRESS)
        
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message.as_string())

        log.info("Email sent successfully!")
        return True
    
    except Exception as e:
        log.error("Error sending email: %s", e)
        return False



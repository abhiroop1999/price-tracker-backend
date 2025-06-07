import smtplib
from email.message import EmailMessage
import os

def send_alert(email, url, price):
    # Safely fetch environment variables with defaults/fallbacks
    EMAIL_USER = os.getenv("EMAIL_USER") or "default@example.com"
    EMAIL_PASS = os.getenv("EMAIL_PASS") or ""
    EMAIL_HOST = os.getenv("EMAIL_HOST") or "smtp.example.com"
    EMAIL_PORT = int(os.getenv("EMAIL_PORT") or "587")

    # Construct the email
    msg = EmailMessage()
    msg.set_content(f"Price dropped to ${float(price):.2f} for {url}")
    msg["Subject"] = "Price Alert"
    msg["From"] = EMAIL_USER
    msg["To"] = email

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
    except Exception as e:
        raise Exception(f"Failed to send email: {e}")

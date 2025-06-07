import smtplib
from email.message import EmailMessage
import os

def send_alert(email, url, price):
    msg = EmailMessage()
    msg.set_content(f"Price dropped to ${float(price):.2f} for {url}")
    msg["Subject"] = "Price Alert"
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = email

    with smtplib.SMTP(os.getenv("EMAIL_HOST"), int(os.getenv("EMAIL_PORT"))) as server:
        server.starttls()
        server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
        server.send_message(msg)

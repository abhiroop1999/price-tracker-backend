import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_alert(email, url, price):
    message = Mail(
        from_email=os.getenv("EMAIL_USER"),
        to_emails=email,
        subject="📉 Price Alert",
        plain_text_content=f"Hey! The price dropped to ${float(price):.2f} for {url}"
    )
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        sg.send(message)
    except Exception as e:
        raise Exception(f"Failed to send email via SendGrid: {e}")

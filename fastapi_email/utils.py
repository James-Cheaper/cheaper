import secrets
from email.message import EmailMessage
from aiosmtplib import send
import os
from dotenv import load_dotenv

load_dotenv()

def generate_token():
    return secrets.token_urlsafe(32)

async def send_verification_email(to_email, token):
    msg = EmailMessage()
    msg["Subject"] = "Verify your email"
    msg["From"] = os.getenv("SMTP_FROM")
    msg["To"] = to_email
    link = f"{os.getenv('SITE_URL')}/verify/{token}"
    msg.set_content(f"Click the link to verify your email:\n{link}")

    await send(
        msg,
        hostname=os.getenv("SMTP_HOST"),
        port=int(os.getenv("SMTP_PORT")),
        username=os.getenv("SMTP_USER"),
        password=os.getenv("SMTP_PASS"),
        start_tls=True,
    )

async def send_confirmation_email(to_email):
    msg = EmailMessage()
    msg["Subject"] = "Email Successfully Verified"
    msg["From"] = os.getenv("SMTP_FROM")
    msg["To"] = to_email
    msg.set_content("Thanks for verifying your email. You're all set!")

    await send(
        msg,
        hostname=os.getenv("SMTP_HOST"),
        port=int(os.getenv("SMTP_PORT")),
        username=os.getenv("SMTP_USER"),
        password=os.getenv("SMTP_PASS"),
        start_tls=True,
    )
"""Email sending utilities."""

from email.mime.text import MIMEText
from smtplib import SMTP
from typing import Optional

from app.core.config import settings


def send_email(
    to_email: str,
    subject: str,
    body: str,
    from_email: Optional[str] = None,
    from_name: Optional[str] = None,
) -> None:
    """Send a simple text email via SMTP.

    Args:
        to_email: Recipient email address.
        subject: Email subject line.
        body: Plain text body.
        from_email: Optional from address (defaults to EMAILS_FROM_EMAIL).
        from_name: Optional from name (defaults to EMAILS_FROM_NAME).
    """
    if not settings.SMTP_HOST or not settings.EMAILS_FROM_EMAIL:
        # Email is not configured; in development we silently skip.
        return

    sender_email = from_email or settings.EMAILS_FROM_EMAIL
    sender_name = from_name or settings.EMAILS_FROM_NAME or settings.PROJECT_NAME

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = to_email

    with SMTP(settings.SMTP_HOST, settings.SMTP_PORT or 587) as smtp:
        if settings.SMTP_USER and settings.SMTP_PASSWORD:
            smtp.starttls()
            smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        smtp.send_message(msg)



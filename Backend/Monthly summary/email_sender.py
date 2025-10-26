# email_sender.py
import smtplib
from email.message import EmailMessage
import config

def send_email(recipient_email, subject, body, message_id=None):
    """
    Sends an email, optionally as a reply to a previous email.

    Args:
        recipient_email (str): The employee's email address.
        subject (str): The subject of the email.
        body (str): The main content of the email (HTML formatted).
        message_id (str, optional): The Message-ID of the original email to reply to.
                                    Defaults to None.
    """
    if not all([config.SENDER_EMAIL, config.SENDER_PASSWORD, config.SMTP_SERVER]):
        print("❌ ERROR: Email credentials or server settings are missing in config/.env.")
        return False

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = config.SENDER_EMAIL
    msg['To'] = recipient_email
    msg.set_content(body, subtype='html')

    # --- MODIFICATION: Add headers to create a reply thread ---
    if message_id:
        msg['In-Reply-To'] = message_id
        msg['References'] = message_id
    # --- END MODIFICATION ---

    try:
        with smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.login(config.SENDER_EMAIL, config.SENDER_PASSWORD)
            server.send_message(msg)
        return True
    except smtplib.SMTPAuthenticationError:
        print("❌ SMTP Authentication Error: Check your email/app password in the .env file.")
        return False
    except Exception as e:
        print(f"❌ An error occurred while sending email to {recipient_email}: {e}")
        return False
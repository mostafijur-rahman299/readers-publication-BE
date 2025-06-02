import smtplib
from config.celery import app
from utils.general_func import send_email
from logging import getLogger

logger = getLogger(__name__)

@app.task(bind=True, default_retry_delay=60)  # retry after 60 seconds
def send_email_task(self, recipients, subject, template, context):
    logger.info(f"Sending email to: {recipients}")
    try:
        send_email(
            subject=subject,
            to_email=recipients,
            html_content=template,
            context=context
        )
    except smtplib.SMTPException as ex:
        logger.error(f"SMTP error sending email: {ex}")
        self.retry(exc=ex)
    except Exception as ex:
        logger.error(f"Unexpected error sending email: {ex}")
        self.retry(exc=ex)

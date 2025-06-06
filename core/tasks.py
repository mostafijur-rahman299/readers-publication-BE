from config.celery import app
from utils.general_func import send_email

@app.task(bind=True, default_retry_delay=60)  # retry after 60 seconds
def send_email_task(self, recipients, subject, template, context):
    try:
        send_email(
            subject=subject,
            to_email=recipients,
            html_content=template,
            context=context
        )
    except Exception as ex:
        self.retry(exc=ex)

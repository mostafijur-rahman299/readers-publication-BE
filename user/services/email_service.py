import random
import string
from core.tasks import send_email_task

class EmailService:
    def generate_code(self, length=6):
        return ''.join(random.choices(string.digits, k=length))

    def send_code(self, subject, template, to_email=[], context={}):
        send_email_task.delay(
            to_email,
		    subject,
		    template,
		    context
		)
        return True

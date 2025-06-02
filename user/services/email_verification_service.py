# services/email_verification_service.py
import uuid
from django.core.mail import send_mail
from django.conf import settings
from .base_verification_service import BaseVerificationService

class EmailVerificationService(BaseVerificationService):
    def generate_code(self):
        return str(uuid.uuid4())

    def send_code(self, user, code):
        link = f"{settings.SITE_URL}/verify-email/{code}/"
        send_mail(
            "Verify Your Email",
            f"Click to verify: {link}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )
        return True

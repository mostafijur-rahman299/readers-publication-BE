import random
from .base_verification_service import BaseVerificationService
from your_twilio_service import send_sms  # abstracted SMS sender

class PhoneVerificationService(BaseVerificationService):
    def generate_code(self):
        return str(random.randint(100000, 999999))

    def send_code(self, user, code):
        pass
        # send_sms(user.phone, f"Your verification code is {code}")

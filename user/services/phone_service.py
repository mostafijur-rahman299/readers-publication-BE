import random
import string

class PhoneService:
    def generate_code(self, length=6):
        return ''.join(random.choices(string.digits, k=length))

    def send_code(self, user, code):
        pass
        # send_sms(user.phone, f"Your verification code is {code}")

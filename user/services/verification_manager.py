# services/verification_manager.py
from user.models import VerificationCode

class VerificationManager:
    def __init__(self, service, type):
        self.service = service
        self.type = type

    def create_and_send_code(self, user):
        code = self.service.generate_code()
        VerificationCode.objects.create(user=user, code=code, type=self.type)
        self.service.send_code(user, code)

    def verify_code(self, user, code_input):
        try:
            record = VerificationCode.objects.filter(user=user, type=self.type).latest('created_at')
        except VerificationCode.DoesNotExist:
            return False, "No code found."

        if record.is_verified:
            return False, "Already verified."
        if record.is_expired():
            return False, "Code expired."
        if record.code != code_input:
            return False, "Invalid code."

        record.is_verified = True
        record.save()
        return True, "Verified."

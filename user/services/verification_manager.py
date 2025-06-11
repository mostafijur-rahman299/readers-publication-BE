from user.models import VerificationCode

class VerificationManager:
    def __init__(self, service, type, **kwargs):
        self.service = service
        self.type = type
        self.kwargs = kwargs

    def create_and_send_code(self, user, code):
        self.service.send_code(
            user=user,
            message=self.kwargs['message'],
            to_numbers=self.kwargs['to_numbers']
        )
        VerificationCode.objects.filter(user=user, type=self.type).delete()
        VerificationCode.objects.create(user=user, code=code, type=self.type)

    def verify_code(self, user, code_input):
        try:
            record = VerificationCode.objects.filter(user=user, type=self.type).latest('created_at')
        except VerificationCode.DoesNotExist:
            return False, "No code found."

        if record.is_used:
            return False, "Already used."
        if record.is_expired():
            return False, "Code expired."
        if record.code != code_input:
            return False, "Invalid code."

        record.is_used = True
        record.save()
        return True, "Verified."

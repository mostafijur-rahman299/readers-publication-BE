from phonenumbers import parse, is_valid_number, format_number, PhoneNumberFormat, NumberParseException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from user.models import User
from user.services.verification_manager import VerificationManager
from user.services.email_service import EmailService
from user.services.phone_service import PhoneService

class ForgotPasswordAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email_or_phone = request.data.get('email_or_phone', None)

        if not email_or_phone:
            return Response({'email_or_phone': 'Email or phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = None
        is_email = False

        # Check if it's a valid email
        if '@' in email_or_phone:
            user = User.objects.filter(email=email_or_phone).first()
            is_email = True
        else:
            try:
                # Try to parse and normalize phone number to E.164
                phone = parse(email_or_phone, "BD")  # BD = Bangladesh
                if is_valid_number(phone):
                    phone_number_e164 = format_number(phone, PhoneNumberFormat.E164)
                    user = User.objects.filter(phone_number=phone_number_e164).first()
                else:
                    return Response({'email_or_phone': 'Invalid phone number'}, status=status.HTTP_400_BAD_REQUEST)
            except NumberParseException:
                return Response({'email_or_phone': 'Invalid phone number format'}, status=status.HTTP_400_BAD_REQUEST)

        if not user:
            return Response({'email_or_phone': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Send verification code here if needed
        if is_email:
            send_code(self, subject, html_content, text_content="", to_email=[], context={})
            verification_manager = VerificationManager(
                EmailService, 'email',
                subject="Forgot Password",
                html_content="",
                text_content="",
                to_email=[user.email],
                context={}
            )
        else:
            verification_manager = VerificationManager(PhoneService, 'phone', user=user, email_or_phone=email_or_phone)
        verification_manager.create_and_send_code(user)

        return Response({'message': 'Code sent to email or phone'}, status=status.HTTP_200_OK)

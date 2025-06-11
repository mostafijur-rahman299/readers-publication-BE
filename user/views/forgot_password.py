from datetime import datetime
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

        try:

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
            code = None
            if is_email:
                email_service = EmailService()
                code = email_service.generate_code()
                verification_manager = VerificationManager(
                    email_service, 'email',
                    subject="Forgot Password",
                    template="email/forgot-password.html",
                    to_email=[user.email],
                    context={
                        'full_name': user.full_name,
                        'year': datetime.now().year,
                        'code': code
                    }
                )
            else:
                phone_service = PhoneService()
                code = phone_service.generate_code()
                message = f"Your verification code is {code}"
                verification_manager = VerificationManager(phone_service, 'phone', user=user, message=message, to_numbers=[str(user.phone_number)])

            # send code
            verification_manager.create_and_send_code(user, code)

        except Exception as e:
            return Response({'non_field_errors': "Something went wrong. Please try again later."}, status=500)

        return Response({'message': 'Code sent to email or phone'}, status=status.HTTP_200_OK)

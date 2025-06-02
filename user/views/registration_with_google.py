# import logging
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# from user.models import User
# from utils.helper_func import generate_tokens_for_user
# from user.api.serializers import UserReadSerializer
# from utils.helper_func import google_get_user_info
# from utils.general_func import get_device_id, is_device_remembered
# from core.tasks import send_email_task
# from django.utils import timezone
# from django.conf import settings
# from user.models.mfa import UserMFA
# from django.core.signing import TimestampSigner

# signer = TimestampSigner(salt='mfa-temp-token')
# logger = logging.getLogger("auth")

# class GoogleLoginView(APIView):
#     def get(self, request, *args, **kwargs):
#         access_token = request.query_params.get('access_token', None)
#         try:
#             user_data = google_get_user_info(access_token=access_token)
#         except:
#             return Response(
#                 {"error": "Failed to obtain user info from Google."},
#                 status=400,
#             )
        
#         # Get the IP address from the request
#         extra = {'ip': request.META.get('REMOTE_ADDR')}
#         logger.info("---------- Login attempt ----------", extra=extra)

#         try:
#             user = User.objects.get(email=user_data["email"])

#             # Check if user is blocked
#             if user.blocked_by_admin:
#                 logger.warning(f"Login blocked: User {user.email} is blocked by admin", extra=extra)
#                 return Response({"non_field_errors": "Your account has been suspended. Please contact support for assistance."}, 
#                                status=status.HTTP_403_FORBIDDEN)
            
#             # Check subscription status
#             if user.subscription_expiration_date and user.subscription_expiration_date < timezone.now():
#                 logger.warning(f"Login blocked: User {user.email} has expired subscription", extra=extra)
#                 return Response({"non_field_errors": "Your subscription has expired. Please contact the admin to renew your subscription."}, 
#                                status=status.HTTP_402_PAYMENT_REQUIRED)

#             # Check email verification if required
#             if user.email_verification_status == False:
#                 logger.warning(f"Login warning: User {user.email} has unverified email", extra=extra)
#                 # Still allow login but include verification status in response

#             # MFA Check
#             mfa, _ = UserMFA.objects.get_or_create(user=user)
#             if mfa.is_enabled:
#                 device_id = get_device_id(request)
#                 if not is_device_remembered(mfa, device_id):
#                     # Not remembered → require MFA
#                     temp_token = signer.sign(user.pk)
#                     if mfa.method == 'totp':
#                         return Response({
#                             "mfa_required": True,
#                             "method": "totp",
#                             "temp_mfa_token": temp_token
#                         }, status=status.HTTP_200_OK)
#                     elif mfa.method == 'email':
#                         mfa.generate_email_otp(user)
#                         return Response({
#                             "mfa_required": True,
#                             "method": "email",
#                             "temp_mfa_token": temp_token,
#                             "message": "OTP sent to your email"
#                         }, status=status.HTTP_200_OK)

#                 else:
#                     logger.info(f"MFA skipped: remembered device {device_id} for user {user.email}", extra=extra)

#             access_token, refresh_token = generate_tokens_for_user(user)
#             response_data = {
#                 "access_token": str(access_token),
#                 "refresh_token": str(refresh_token),
#                 "user": UserReadSerializer(user).data,
#             }
#             return Response(response_data, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             first_name = user_data.get("given_name", "")
#             last_name = user_data.get("family_name", "")
#             email_verification_status = bool(user_data["email_verified"] == 'true')

#             user = User.objects.create(
#                 email=user_data["email"],
#                 first_name=first_name,
#                 last_name=last_name,
#                 email_verification_status=email_verification_status,
#                 registration_method="google",
#             )

#             access_token, refresh_token = generate_tokens_for_user(user)
#             response_data = {
#                 "access_token": str(access_token),
#                 "refresh_token": str(refresh_token),
#                 "user": UserReadSerializer(user).data,
#             }
#             return Response(response_data, status=status.HTTP_200_OK)

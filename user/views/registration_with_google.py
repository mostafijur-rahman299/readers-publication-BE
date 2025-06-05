import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from user.models import User
from utils.helper_func import generate_tokens_for_user
from utils.helper_func import google_get_user_info

class GoogleLoginView(APIView):
    def post(self, request, *args, **kwargs):
        access_token = request.data.get('access_token', None)
        try:
            user_data = google_get_user_info(access_token=access_token)
        except:
            return Response(
                {"non_field_errors": "Failed to obtain user info from Google."},
                status=400,
            )

        try:
            user = User.objects.get(email=user_data["email"])

            access_token, refresh_token = generate_tokens_for_user(user)
            response_data = {
                "access_token": str(access_token),
                "refresh_token": str(refresh_token)
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            first_name = user_data.get("given_name", "")
            last_name = user_data.get("family_name", "")

            user = User.objects.create(
                email=user_data["email"],
                full_name=f"{first_name} {last_name}",
                is_email_verified=True
            )

            access_token, refresh_token = generate_tokens_for_user(user)
            response_data = {
                "access_token": str(access_token),
                "refresh_token": str(refresh_token),
            }
            return Response(response_data, status=status.HTTP_200_OK)

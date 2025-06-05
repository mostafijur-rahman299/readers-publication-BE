from django.urls import path
from user.views import UserRegistrationAPIView


urlpatterns = [
    # User Registration
    path('api/v1/auth/registration/', UserRegistrationAPIView.as_view(), name='user-registration'),
]

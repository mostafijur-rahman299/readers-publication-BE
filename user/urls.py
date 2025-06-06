from django.urls import path
from user.views import UserRegistrationAPIView
from user.views import GoogleLoginView
from user.views import ForgotPasswordAPIView

urlpatterns = [
    # User Registration
    path('api/v1/auth/registration/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('api/v1/auth/google-login/', GoogleLoginView.as_view(), name='google-login'),
    path('api/v1/auth/forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
]

from django.urls import path
from user.views import UserRegistrationAPIView
from user.views import GoogleLoginView

urlpatterns = [
    # User Registration
    path('api/v1/auth/registration/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('api/v1/auth/google-login/', GoogleLoginView.as_view(), name='google-login'),
]

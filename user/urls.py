from django.urls import path
from user.views import UserRegistrationAPIView


urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
]

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from user.serializers import UserRegistrationSerializer


class UserRegistrationAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        refresh = RefreshToken.for_user(serializer.instance)

        data = {
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token)
        }

        return Response(data, status=status.HTTP_201_CREATED)



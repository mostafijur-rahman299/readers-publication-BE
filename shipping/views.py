from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import Shipping
from .serializers import ShippingCreateSerializer, ShippingReadSerializer
from rest_framework.permissions import IsAuthenticated

class ShippingModelViewSet(ModelViewSet):
    queryset = Shipping.objects.all()
    serializer_class = ShippingReadSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return ShippingCreateSerializer
        return ShippingReadSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


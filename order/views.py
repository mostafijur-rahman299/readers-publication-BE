from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderCreateSerializer, OrderListSerializer
from rest_framework.permissions import IsAuthenticated
from core.pagination import GeneralPagination

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = GeneralPagination
    
    def get_queryset(self):
        status = self.request.query_params.get('status', 'all')
        if status == 'all':
            return Order.objects.filter(user=self.request.user)
        
        print(status)
        return Order.objects.filter(user=self.request.user, status=status)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        return OrderCreateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"order_id": serializer.data['order_id']}, status=status.HTTP_201_CREATED, headers=headers)


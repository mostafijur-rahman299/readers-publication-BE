from cart.models import Cart
from cart.serializers import CartSerializerRead
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

class CartView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    serializer_class = CartSerializerRead
    lookup_field = 'uuid'

    def get_queryset(self):
        return Cart.objects.filter(is_active=True, user=self.request.user)

    def get_serializer_class(self):
        return CartSerializerRead

    @action(detail=True, methods=['patch'])
    def update_quantity(self, request, uuid=None):
        cart = get_object_or_404(Cart, uuid=uuid, is_active=True)

        quantity = request.data.get('quantity')
        if quantity is not None:
            try:
                quantity = int(quantity)
                if quantity < 1:
                    return Response({'error': 'Quantity must be at least 1'}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({'error': 'Quantity must be an integer'}, status=status.HTTP_400_BAD_REQUEST)

            cart.quantity = quantity
            cart.save()
            return Response(CartSerializerRead(cart).data, status=status.HTTP_200_OK)

        return Response({'error': 'Quantity is required'}, status=status.HTTP_400_BAD_REQUEST)

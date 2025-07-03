from django.shortcuts import render
from cart.models import Cart
from cart.serializers import CartSerializerRead
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class CartView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = Cart.objects.filter(is_active=True)
        serializer = CartSerializerRead(cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = CartSerializerRead(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

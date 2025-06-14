from rest_framework import viewsets
from .models import Book, Category
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookSerializer, CategorySerializer

class CategoryViewSet(viewsets.ViewSet):
    def list(self, request):
        categories = Category.objects.filter(is_active=True).order_by('index_number')
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)



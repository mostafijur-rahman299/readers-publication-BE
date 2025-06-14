from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from book.models import Book, BookImage
from book.serializers import BookSerializerListRead

class BookViewSet(viewsets.ViewSet):
    def list(self, request):
        books = Book.objects.filter(is_active=True).order_by('index_number')
        serializer = BookSerializer(books, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
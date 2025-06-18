from rest_framework.generics import ListAPIView
from book.models import Book
from book.serializers.book import BookSerializerRead

class BookListAPIView(ListAPIView):
    serializer_class = BookSerializerRead
    queryset = Book.objects.all()

    def get_queryset(self):
        return Book.objects.filter(status='published')

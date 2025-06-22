from rest_framework.generics import ListAPIView
from book.models import Book
from book.serializers.book import BookSerializerListRead
from core.pagination import GeneralPagination
from rest_framework.response import Response

class BookListAPIView(ListAPIView):
    serializer_class = BookSerializerListRead
    queryset = Book.objects.all()
    pagination_class = GeneralPagination

    def get_queryset(self):
        return Book.objects.filter(is_active=True).order_by('-published_date')

    def get_paginated_response(self, data):
        # If pagination is off, return all data in a single response
        is_pagination_off = self.request.query_params.get('pagination', 'true')
        if is_pagination_off == 'false':
            return Response(data)
        return super().get_paginated_response(data)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

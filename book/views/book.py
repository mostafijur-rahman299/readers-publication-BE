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
        is_featured = self.request.query_params.get("is_featured")

        # Home pase featured data
        if is_pagination_off == 'false' and is_featured == "true":

            qs = Book.objects.filter(is_active=True).order_by('-published_date')
            new_arrival = qs.filter(is_new_arrival=True)
            popular = qs.filter(is_popular=True)
            comming_soon = qs.filter(is_comming_soon=True)
            best_seller = qs.filter(is_best_seller=True)

            data = {
                "new_arrival": BookSerializerListRead(new_arrival, many=True).data,
                "popular": BookSerializerListRead(popular, many=True).data,
                "comming_soon": BookSerializerListRead(comming_soon, many=True).data,
                "best_seller": BookSerializerListRead(best_seller, many=True).data,
            }

            return Response(data)
        return super().get_paginated_response(data)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

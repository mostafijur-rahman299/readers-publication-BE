from rest_framework.generics import ListAPIView, RetrieveAPIView
from book.models import Book, BookPreview
from book.serializers.book import BookSerializerListRead, BookSerializerDetailRead, BookPreviewSerializerListRead
from core.pagination import GeneralPagination
from rest_framework.response import Response

class BookListAPIView(ListAPIView):
    serializer_class = BookSerializerListRead
    queryset = Book.objects.all()
    pagination_class = GeneralPagination

    def get_queryset(self):
        category = self.request.query_params.getlist("category[]")
        author = self.request.query_params.getlist("author[]")
        price_min = self.request.query_params.get("price[min]")
        price_max = self.request.query_params.get("price[max]")

        queryset = Book.objects.all()

        # sort by
        sort_by = self.request.query_params.get("sort_by")
        if sort_by == "recent":
            queryset = queryset.order_by('-published_date', '-created_at')
        elif sort_by == "popular":
            queryset = queryset.order_by('-rating', '-created_at')
        elif sort_by == "price_low_to_high":
            queryset = queryset.order_by('price')
        elif sort_by == "price_high_to_low":
            queryset = queryset.order_by('-price')


        if category:
            queryset = queryset.filter(categories__id__in=category).distinct()
        if author:
            queryset = queryset.filter(author__id__in=author).distinct()
        if price_min and int(price_min) > 0:
            price_min = int(price_min)
            queryset = queryset.filter(price__gte=price_min).distinct()
        if price_max and int(price_max) > 0:
            price_max = int(price_max)
            queryset = queryset.filter(price__lte=price_max).distinct()

        return queryset.filter(is_active=True)
    
    def paginate_queryset(self, queryset):
        self.pagination_class.page_size = 20
        return super().paginate_queryset(queryset)
    
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
    

class BookDetailAPIView(RetrieveAPIView):
    serializer_class = BookSerializerDetailRead
    queryset = Book.objects.all()
    lookup_field = "slug"

    def get_object(self):
        return super().get_object()
    

class BookPreviewAPIView(ListAPIView):
    serializer_class = BookPreviewSerializerListRead
    queryset = BookPreview.objects.all()
    pagination_class = GeneralPagination

    def get_queryset(self): 
        return BookPreview.objects.filter(book_id=self.kwargs['book_id'], is_active=True).order_by('index_number')


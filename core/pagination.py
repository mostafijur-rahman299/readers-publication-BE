from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class GeneralPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'page_number': self.page.number,
            'page_range': list(self.page.paginator.page_range),
            'results': data
        })


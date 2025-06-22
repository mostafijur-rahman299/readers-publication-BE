from django.urls import path
from book.views.category import CategoryListAPIView
from book.views.book import BookListAPIView

urlpatterns = [
    path('api/v1/categories/', CategoryListAPIView.as_view(), name='book-categories-list'),
    path('api/v1/list/', BookListAPIView.as_view(), name='book-list'),
]

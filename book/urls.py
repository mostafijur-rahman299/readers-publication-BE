from django.urls import path
from book.views.category import CategoryListAPIView

urlpatterns = [
    path('api/v1/categories/', CategoryListAPIView.as_view(), name='book-categories-list'),
]

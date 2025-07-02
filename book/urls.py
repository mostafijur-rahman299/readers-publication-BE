from django.urls import path
from book.views.category import CategoryListAPIView
from book.views.book import BookListAPIView, BookDetailAPIView, BookPreviewAPIView
from book.views.special_package import SpecialPackageListAPIView


urlpatterns = [
    path('api/v1/categories/', CategoryListAPIView.as_view(), name='book-categories-list'),
    path('api/v1/list/', BookListAPIView.as_view(), name='book-list'),
    path('api/v1/special-packages/', SpecialPackageListAPIView.as_view(), name='special-package-list'),
    path('api/v1/detail/<slug:slug>/', BookDetailAPIView.as_view(), name='book-detail'),
    path('api/v1/previews/<int:book_id>/', BookPreviewAPIView.as_view(), name='book-previews'),
]

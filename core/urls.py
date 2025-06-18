from django.urls import path
from .views import SupportCreateView, GeneralDataRetrieveView, CarouselListAPIView

urlpatterns = [
    path('api/v1/support/', SupportCreateView.as_view(), name='support-create'),
    path('api/v1/general-data/', GeneralDataRetrieveView.as_view(), name='general-data-retrieve'),
    path('api/v1/carousel/', CarouselListAPIView.as_view(), name='carousel-list'),
]
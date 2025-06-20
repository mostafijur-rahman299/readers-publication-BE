from django.urls import path
from .views import CarouselListViewSet, get_general_data, TestimonialListAPIView

urlpatterns = [
    # path('api/v1/support/', SupportCreateView.as_view(), name='support-create'),
    path('api/v1/general-data/', get_general_data, name='general-data-retrieve'),
    path('api/v1/home-carousel/', CarouselListViewSet.as_view({'get': 'list'}), name='home-carousel-list'),
    path('api/v1/testimonials/', TestimonialListAPIView.as_view(), name='testimonial-list')
]
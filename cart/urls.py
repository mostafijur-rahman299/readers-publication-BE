from django.urls import path
from cart.views import CartView

urlpatterns = [
    path('api/v1/list/', CartView.as_view(), name='cart-list'),
]
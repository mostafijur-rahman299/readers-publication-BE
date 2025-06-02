from django.db import models

from core.models import BaseModel
from user.models import User
from shipping.models import Shipping
from payment.models import Payment


class OrderStatus(models.TextChoices):
    PENDING = 'pending'
    PAID = 'paid'
    CONFIRMED = 'confirmed'
    PACKED = 'packed'
    READY_TO_SHIP = 'ready_to_ship'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default='pending')
    shipping_address = models.ForeignKey(Shipping, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.total_amount}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-created_at']


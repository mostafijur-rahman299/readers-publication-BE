from django.db import models

from core.models import BaseModel
from user.models import User


class PaymentMethod(models.TextChoices):
    CASH_ON_DELIVERY = 'cash_on_delivery'
    BANK_TRANSFER = 'bank_transfer'
    BKASH = 'bkash'
    ROCKET = 'rocket'
    NAGAD = 'nagad'


class PaymentStatus(models.TextChoices):
    PENDING = 'pending'
    PAID = 'paid'
    FAILED = 'failed'


class Payment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default='cash_on_delivery')
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    payment_url = models.URLField(blank=True, null=True)
    payment_response = models.JSONField(blank=True, null=True)
    payment_response_code = models.CharField(max_length=255, blank=True, null=True)
    payment_response_message = models.TextField(blank=True, null=True)

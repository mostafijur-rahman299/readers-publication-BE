from django.db import models

from core.models import BaseModel, Country, State, City, Thana
from user.models import User


class Shipping(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipping', null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='shipping', null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='shipping', null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='shipping', null=True, blank=True)
    thana = models.ForeignKey(Thana, on_delete=models.CASCADE, related_name='shipping', null=True, blank=True)
    detail_address = models.CharField(max_length=255, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Shipping"
        verbose_name_plural = "Shipping"
        ordering = ['-created_at']

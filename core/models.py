from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Carousel(BaseModel):
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='carousel_images/')
    link = models.URLField(blank=True, null=True)
    is_advertise = models.BooleanField(default=False)

    def __str__(self):
        return self.title if self.title else "Carousel Image"

    class Meta:
        verbose_name = "Carousel"
        verbose_name_plural = "Carousels"
        ordering = ['-created_at']  # Order by creation date descending
        
    def clean(self):
        if Carousel.objects.filter(is_advertise=True).count() > 2 and self.is_advertise:
            raise ValueError("Only up to 2 carousel items can be marked as advertisements.")
        return super().clean()

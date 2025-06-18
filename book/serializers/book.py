from rest_framework import serializers
from book.models import Book
from django.conf import settings

class BookSerializerRead(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name')
    cover_image_url = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ["title", "title_bn", "author_name", "price", "discounted_price", "cover_image_url", "rating", "rating_count", "discount_percentage", "is_available"]

    def get_cover_image_url(self, obj):
        return f"{settings.BACKEND_SITE_HOST}{obj.cover_image.url}" if obj.cover_image else ""

    def get_discount_percentage(self, obj):
        if obj.discounted_price:
            return int(((obj.price - obj.discounted_price) / obj.price) * 100)
        return 0

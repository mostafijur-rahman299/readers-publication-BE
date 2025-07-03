from rest_framework import serializers
from cart.models import Cart
from django.conf import settings

class CartSerializerRead(serializers.ModelSerializer):
    book_details = serializers.SerializerMethodField()
    author_details = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'uuid',
            'quantity',
            'book_details',
            'author_details',
        ]

    def get_book_details(self, obj):
        return {
            'id': obj.book.id,
            'slug': obj.book.slug,
            'title': obj.book.title,
            'title_bn': obj.book.title_bn,
            'cover_image': f"{settings.BACKEND_HOST}{obj.book.cover_image}" if obj.book.cover_image else None,
            "price": obj.book.price,
            "discounted_price": obj.book.discounted_price,
            "is_active": obj.book.is_active,
            'is_available': obj.book.is_available
        }
    
    def get_author_details(self, obj):
        return {
            'id': obj.book.author.id,
            'name': obj.book.author.name,
            'name_bn': obj.book.author.name_bn,
        }
    

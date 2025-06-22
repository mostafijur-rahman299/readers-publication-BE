from rest_framework import serializers
from book .models import Book, Category
from django.conf import settings

class BookSerializerListRead(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField(required=False)
    author_full_name = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'title_bn', 'author_full_name', 'cover_image', 'price', 'discounted_price', "discount",
            'rating', 'rating_count', 'is_available', "is_new_arrival", "is_popular", "is_comming_soon"
        ]

    def get_cover_image(self, obj):
        if obj.cover_image:
            return f"{settings.BACKEND_SITE_HOST}{obj.cover_image.url}"
        return None

    def get_discount(self, obj):
        if obj.discounted_price and obj.discounted_price < obj.price:
            return round((obj.price - obj.discounted_price) / obj.price * 100, 2)
        return 0.0
    
    def get_author_full_name(self, obj):
        return obj.author.user.get_full_name()

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Category
        fields =  ['name', 'description', 'image']  # or specify fields like ('id', 'name', 'description')

    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

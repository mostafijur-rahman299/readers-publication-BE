from rest_framework import serializers
from .models import Book, Category

class BookSerializerListRead(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField(required=False)
    author__full_name = serializers.CharField(source='author.full_name', read_only=True)
    discount = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author__full_name', 'cover_image', 'price', 'discount_price', "discount"
            'rating', 'rating_count', 'is_available', 'sku', "is_new"
        ]

    def get_cover_image(self, obj):
        if obj.cover_image:
            return self.context['request'].build_absolute_uri(obj.cover_image)
        return None

    def get_discount(self, obj):
        if obj.discounted_price and obj.discounted_price < obj.price:
            return round((obj.price - obj.discounted_price) / obj.price * 100, 2)
        return 0.0

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodFeild(required=False)

    class Meta:
        model = Category
        fields =  ['name', 'description', 'image']  # or specify fields like ('id', 'name', 'description')

    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

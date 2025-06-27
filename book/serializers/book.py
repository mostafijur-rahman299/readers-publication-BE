from rest_framework import serializers
from book.models import Book, Category
from django.conf import settings

class BookSerializerListRead(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField(required=False)
    author_full_name = serializers.SerializerMethodField()
    author_full_name_bn = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'slug', 'title', 'title_bn', 'author_full_name', 'author_full_name_bn', 'cover_image', 'price', 'discounted_price',
            'rating', 'rating_count', 'is_available', "is_new_arrival", "is_popular", "is_comming_soon"
        ]

    def get_cover_image(self, obj):
        if obj.cover_image:
            return f"{settings.BACKEND_SITE_HOST}{obj.cover_image.url}"
        return None
    
    def get_author_full_name(self, obj):
        return obj.author.name

    def get_author_full_name_bn(self, obj):
        return obj.author.name_bn if obj.author.name_bn else obj.author.name
    
    def get_price(self, obj):
        return int(obj.price)
    
    def get_discounted_price(self, obj):
        return int(obj.discounted_price) if obj.discounted_price else None

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Category
        fields =  ['name', 'description', 'image']  # or specify fields like ('id', 'name', 'description')

    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None
    

class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields =  [
            'id', 'slug', 'title', 'title_bn', 'author_full_name', 'author_full_name_bn', 'cover_image', 'price', 'discounted_price',
            'rating', 'rating_count', 'is_available', "is_new_arrival", "is_popular", "is_comming_soon"
        ]


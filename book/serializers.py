from rest_framework import serializers
from .models import Book, Category

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # or specify fields like ('id', 'title', 'author', 'published_date')

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodFeild(required=False)

    class Meta:
        model = Category
        fields =  ['name', 'description', 'image']  # or specify fields like ('id', 'name', 'description')

    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

from rest_framework import serializers
from .models import Author

class AuthorSerializerListRead(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    profile_picture = serializers.SerializerMethodField(required=False)
    number_of_books = serializers.IntegerField(source='user.books.count', read_only=True)
   
    class Meta:
        model = Author
        fields = [
            'id', 'full_name', 'profile_picture', 'number_of_books'
        ]

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return self.context['request'].build_absolute_uri(obj.profile_picture.url)
        return None

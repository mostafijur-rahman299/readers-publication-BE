from rest_framework import serializers
from .models import Author

class AuthorSerializerListRead(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField(required=False)
   
    class Meta:
        model = Author
        fields = [
            'id', 'name', 'name_bn', 'profile_picture'
        ]

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return self.context['request'].build_absolute_uri(obj.profile_picture.url)
        return None

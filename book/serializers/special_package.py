from rest_framework import serializers
from book.models import SpecialPackage
from django.conf import settings

class SpecialPackageSerializerListRead(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(required=False)

    class Meta:
        model = SpecialPackage
        fields = [
            'uuid', 'image'
        ]

    def get_image(self, obj):
        if obj.image:
            return f"{settings.BACKEND_SITE_HOST}{obj.image.url}"
        return None

from rest_framework import serializers
from .models import Support, GeneralData, Carousel
from django.conf import settings

class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = ['name', 'email', 'phone', 'message']


class GeneralDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralData
        fields = ['address', 'phone', 'email', 'facebook', 'twitter', 'instagram', 'youtube']


class CarouselSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Carousel
        fields = ['title', 'title_bn', 'subtitle', 'subtitle_bn', 'image_url', 'link', 'is_advertise']

    def get_image_url(self, obj):
        return f"{settings.BACKEND_SITE_HOST}{obj.image.url}" if obj.image else ""


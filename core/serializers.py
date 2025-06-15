from serializers import ModelSerializer
from .models import Carousel


class CarouselSerializer(ModelSerializer):
    image = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Carousel
        fields = ['title', 'title_bn', 'subtitle', 'subtitle_bn', 'image', 'link', 'is_advertise']  # or specify fields like ('id', 'title', 'image', 'is_advertise')

    def get_image(self, obj):
        if obj.image:
            return f"{settings.SITE_HOST}{obj.image.url}" if obj.image else ""
        return None

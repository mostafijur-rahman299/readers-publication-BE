from rest_framework import serializers
from .models import Shipping

class ShippingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = ['name', 'phone', 'email', 'state', 'city', 'thana', 'note', 'detail_address', 'is_default', 'address_type']

        extra_kwargs = {
            'state': {'required': True, 'allow_null': False},
            'city': {'required': True, 'allow_null': False},
            'thana': {'required': True, 'allow_null': False},
            'detail_address': {'required': True, 'allow_null': False},
            'note': {'required': False, 'allow_null': True},
            'is_default': {'required': False, 'allow_null': True},
            'name': {'required': True, 'allow_null': False},
            'phone': {'required': True, 'allow_null': False},
            'email': {'required': False, 'allow_null': True},
            'address_type': {'required': True, 'allow_null': False},
        }

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ShippingReadSerializer(serializers.ModelSerializer):
    state = serializers.CharField(source='state.name', read_only=True)
    city = serializers.CharField(source='city.name', read_only=True)
    thana = serializers.CharField(source='thana.name', read_only=True)
    address_type = serializers.CharField(source='get_address_type_display', read_only=True)
    
    class Meta:
        model = Shipping
        fields = ['name', 'phone', 'email', 'state', 'city', 'thana', 'detail_address', 'note', 'is_default', 'address_type']

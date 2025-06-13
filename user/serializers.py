import phonenumbers
from rest_framework import serializers
from django.conf import settings
from user.models import User, UserProfile
from django.core.validators import EmailValidator

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number', 'password', 'confirm_password']
        extra_kwargs = {
            'email': {'required': True, 'validators': [EmailValidator()]},
            'password': {'write_only': True, 'required': True},
            'confirm_password': {'write_only': True, 'required': True},
            'full_name': {'required': True, 'min_length': 3},
        }

    def validate_phone_number(self, value):
        if not value:
            return value
        
        try:
            parsed_number = phonenumbers.parse(value, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise serializers.ValidationError("Invalid phone number.")
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError("Invalid phone number format.")
        
        is_exist = User.objects.filter(phone_number=value).exists()
        if is_exist:
            if self.instance and self.instance.phone_number == value:
                return value
            else:
                raise serializers.ValidationError("Phone number already exists.")
        
        return value
    
    def validate_email(self, value):
        is_exist = User.objects.filter(email=value).exists()
        if is_exist:
            if self.instance and self.instance.email == value:
                return value
            else:
                raise serializers.ValidationError("Email already exists.")
        
        return value
        
    def validate(self, data):     
        if data['password'] != data.pop('confirm_password'):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        
        return user


class UserProfileSerializerRead(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    joined_at = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'address', 'full_name', 'email', 'phone_number', 'joined_at', 'profile_picture']

    def get_full_name(self, instance):
        return instance.user.full_name if instance.user.full_name else instance.user.username or instance.user.email.split('@')[0]

    def get_email(self, instance):
        return instance.user.email if instance.user.email else ""

    def get_phone_number(self, instance):
        return str(instance.user.phone_number) if instance.user.phone_number else ""
    
    def get_joined_at(self, instance):
        return instance.user.date_joined.strftime("%d %b, %Y")

    def get_profile_picture(self, instance):
        return settings.BACKEND_SITE_HOST + instance.profile_picture.url if instance.profile_picture else None

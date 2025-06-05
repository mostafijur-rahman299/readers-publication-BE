import phonenumbers
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from core.tasks import send_email_task
from user.models import User
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

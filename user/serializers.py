from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from core.tasks import send_email_task
from user.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate_password(self, password):
        try:
            validate_password(password)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"password": e.detail})
        return password
        
    def validate(self, data):     
        if data['password'] != data.pop('confirm_password'):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})        
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        
        return user

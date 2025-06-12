from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from datetime import timedelta

from core.models import BaseModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        # Create and save a User with the given email and password.

        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        # Create and save a SuperUser with the given email and password.

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        # for user id(email) case insensitive
        case_insensitive_username_field = "{}__iexact".format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: email})


class User(BaseModel, AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others')
    ]

    username = models.CharField(max_length=50)
    email = models.EmailField(db_collation="case_insensitive", unique=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, null=True)
    date_of_birth = models.DateField(null=True)
    
    is_email_verified = models.BooleanField(default=False)

    objects = UserManager()

    def __str__(self):
        return self.full_name if self.full_name else self.email.split('@')[0]


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


class VerificationCode(BaseModel):
    TYPE_EMAIL = 'email'
    TYPE_PHONE = 'phone'
    TYPE_2FA = '2fa'

    VERIFICATION_TYPE_CHOICES = [
        (TYPE_EMAIL, 'Email'),
        (TYPE_PHONE, 'Phone'),
        (TYPE_2FA, 'Two-Factor'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=VERIFICATION_TYPE_CHOICES)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        expiry_map = {
            self.TYPE_EMAIL: timedelta(hours=24),
            self.TYPE_PHONE: timedelta(minutes=30),
            self.TYPE_2FA: timedelta(minutes=5),
        }
        return timezone.now() > self.created_at + expiry_map[self.type]
    
    def verify_code(self, code_input):
        if self.is_expired():
            return False
        if self.is_used:
            return False
        if self.code == code_input:
            self.is_used = True
            self.save()
            return True
        return False


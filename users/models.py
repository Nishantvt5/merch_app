# users/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers 
    and make it easier to create customers and administrators.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        
        # Ensure 'is_customer' is False for admins
        extra_fields.setdefault('is_customer', False)

        return self.create_user(email, password, **extra_fields)

# Custom User Model definition
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for separating customer and admin roles.
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    # Role-specific fields
    is_customer = models.BooleanField(default=True)  # Default for new users
    is_admin = models.BooleanField(default=False)    # For shop administrators

    # Required for Django admin and permissions
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Only email is required for superuser creation

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email

    # Additional methods to check roles
    def is_store_admin(self):
        return self.is_admin

    def is_regular_customer(self):
        return self.is_customer
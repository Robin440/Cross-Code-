
from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import TimestampedModel
import uuid

class CustomUser(AbstractUser, TimestampedModel):
    """Custom user model extending AbstractUser with additional fields."""
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,primary_key=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True,unique=True)
    verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'


    def __str__(self):
        return f"User : {self.username} -- ({self.email})"
    
    class Meta:
        db_table = 'custom_user'
        verbose_name = 'Custom User'



class Verification(models.Model):
    """Model to store verification tokens and OTPs for users."""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    otp = models.CharField(max_length=6, blank=True, null=True)
    purpose = models.CharField(max_length=50)  # e.g., 'email_verification', 'password_reset'
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    def __str__(self):
        return f"Verification for {self.user.email} - Purpose: {self.purpose}"
    
    class Meta:
        db_table = 'verification'
        verbose_name = 'Verification'
        indexes = [
            models.Index(fields=['user', 'purpose']),
            models.Index(fields=['token']),
            models.Index(fields=['otp']),
        ]

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    verified = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['phone_number']

    def save(self, *args, **kwargs):
        if not self.username:  # Set username to phone_number if it's not already set
            self.username = self.phone_number
        if self._state.adding and not self.password:
            self.password = make_password('defaultpassword123')  # Default password for new users
        super().save(*args, **kwargs)

    def __str__(self):
        return self.phone_number


class Trip(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    museum_name = models.CharField(max_length=255)
    visitors_info = models.JSONField()
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Store phone number for now

    def __str__(self):
        return f"{self.user.phone_number} - {self.museum_name} Trip"

class Museum(models.Model):
    MUSEUM_NAME = models.CharField(max_length=200, null=True)
    PINCODE = models.IntegerField(default=132001, null=True)
    ADULTPRICE = models.IntegerField(null=True)
    CHILDPRICE = models.IntegerField(null=True)

    def __str__(self):
        return self.MUSEUM_NAME
    

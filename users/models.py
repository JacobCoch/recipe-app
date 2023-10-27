from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class CustomUser(AbstractUser):
    # Add custom fields to your user model

    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"username": self.username})
    
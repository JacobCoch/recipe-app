from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class CustomUser(AbstractUser):
    # Add custom fields to your user model
    pic = models.ImageField(upload_to="profile_pics", blank=True, null=True, default="no_picture.jpg")
    bio = models.TextField(blank=True, null=True)
    liked_recipes = models.ManyToManyField('recipes.Recipe', through='recipes.SavedRecipe', related_name='users_who_liked')
    
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"username": self.username})
    

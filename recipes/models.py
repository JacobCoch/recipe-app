import logging
from django.contrib.auth.models import Group, Permission
from django.conf import settings
# Create your models here.
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class Recipe(models.Model):
    name = models.CharField(max_length=50)
    ingredients = models.CharField(max_length=255)
    cooking_time = models.IntegerField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    pic = models.ImageField(upload_to="recipes", default="no_picture.jpg")

    def __str__(self):
        return f"""
        {self.name}
        Ingredients: {self.ingredients}
        Cooking Time: {self.cooking_time} minutes
        Difficulty: {self.calc_difficulty()}
        """

    def calc_difficulty(self):
        difficulty_levels = {
            "Easy": "Easy",
            "Medium": "Medium",
            "Intermediate": "Intermediate",
            "Hard": "Hard",
        }

        ingredients_list = self.ingredients.split(", ")
        num_ingredients = len(ingredients_list)

        if self.cooking_time < 10:
            if num_ingredients < 4:
                difficulty = difficulty_levels.get("Easy")
            else:
                difficulty = difficulty_levels.get("Medium")
        else:
            if num_ingredients < 4:
                difficulty = difficulty_levels.get("Intermediate")
            else:
                difficulty = difficulty_levels.get("Hard")

            # Log the difficulty level
            logging.info(f"Recipe difficulty for {self.name}: {difficulty}")

        return difficulty

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        self.ingredients = self.ingredients.title()
        super(Recipe, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("recipes:detail", kwargs={"pk": self.pk})


class CustomUser(AbstractUser):
    # Add custom fields to your user model
    pic = models.ImageField(
        upload_to="profile_pics", blank=True, null=True, default="no_picture.jpg"
    )
    bio = models.TextField(blank=True, null=True)
    fav_recipes = models.ManyToManyField(
        Recipe, blank=True, related_name="users_favorites"
    )


    # Add related_name to resolve clashes
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name="customuser_set",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="customuser_set",
    )


    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("recipes:profile", kwargs={"username": self.username})

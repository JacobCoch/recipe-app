from django.db import models
from django.urls import reverse

# Create your models here.
from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=50)
    ingredients = models.CharField(max_length=255)
    cooking_time = models.IntegerField()

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
            "Easy": "Easy 😄",
            "Medium": "Medium 😅",
            "Intermediate": "Intermediate 😓",
            "Hard": "Hard 😰",
        }

        if (self.cooking_time < 10) and (len(self.ingredients) < 4):
            return difficulty_levels.get("Easy")
        elif (self.cooking_time < 10) and (len(self.ingredients) >= 4):
            return difficulty_levels.get("Medium")
        elif (self.cooking_time >= 10) and (len(self.ingredients) < 4):
            return difficulty_levels.get("Intermediate")
        elif (self.cooking_time >= 10) and (len(self.ingredients) >= 4):
            return difficulty_levels.get("Hard")
        else:
            print("Something bad happened, please try again")

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        self.ingredients = self.ingredients.title()
        super(Recipe, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("recipes:detail", kwargs={"pk": self.pk})

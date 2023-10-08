from django.db import models

# Create your models here.
class Recipe(models.Model):
  name = models.CharField(max_length=50)
  ingredients =  models.CharField(max_length=255)
  cooking_time = models.IntegerField()

  DIFFICULTY_CHOICES = [
        ('Easy', 'Easy 😄'),
        ('Medium', 'Medium 😅'),
        ('Intermediate', 'Intermediate 😓'),
        ('Hard', 'Hard 😰'),
    ]
  difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)

  def __str__(self):
    return f"""
    Name: {self.name}
    Ingredients: {self.ingredients}
    Cooking Time: {self.cooking_time} minutes
    Difficulty: {self.get_difficulty_display()}
    """
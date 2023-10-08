from django.test import TestCase
from .models import Recipe
# Create your tests here.
class RecipeModelTest(TestCase):
  def setUpTestData():
    Recipe.objects.create(name='Pasta', ingredients='flour, water, salt', cooking_time=30, difficulty='Easy')

  def test_recipe_content(self):
    recipe = Recipe.objects.get(id=1)

    field_label = recipe._meta.get_field('name').verbose_name

    self.assertEquals(field_label, 'name')
    self.assertEquals(recipe.name, 'Pasta')
    self.assertEquals(recipe.ingredients, 'flour, water, salt')
    self.assertEquals(recipe.cooking_time, 30)
    self.assertEquals(recipe.difficulty, 'Easy')
    self.assertEquals(recipe.get_difficulty_display(), 'Easy 😄')

  def test_recipe_str(self):
    recipe = Recipe.objects.get(id=1)
    self.assertEquals(str(recipe), """
    Name: Pasta
    Ingredients: flour, water, salt
    Cooking Time: 30 minutes
    Difficulty: Easy 😄
    """)
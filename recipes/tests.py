from django.test import TestCase
from .models import Recipe


# Create your tests here.
class RecipeModelTest(TestCase):
    def setUpTestData():
        Recipe.objects.create(
            name="Pasta", ingredients="flour, water, salt, eggs", cooking_time=10
        )

    def test_name_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "name")

    def test_ingredients_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field("ingredients").verbose_name
        self.assertEquals(field_label, "ingredients")

    def test_cooking_time_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field("cooking_time").verbose_name
        self.assertEquals(field_label, "cooking time")

    def test_pic_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field("pic").verbose_name
        self.assertEquals(field_label, "pic")

    def test_name_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field("name").max_length
        self.assertEquals(max_length, 50)

    def test_ingredients_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field("ingredients").max_length
        self.assertEquals(max_length, 255)

    def test_cooking_time(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEquals(recipe.cooking_time, 10)

    def test_difficulty(self):
        recipe = Recipe.objects.get(id=1)
        recipe.cooking_time = 5
        recipe.ingredients = "flour, water, salt, eggs"
        self.assertEquals(recipe.calc_difficulty(), "Medium")

    def test_save(self):
        recipe = Recipe.objects.get(id=1)
        recipe.name = "pancakes"
        recipe.ingredients = "flour, milk, eggs, sugar"
        recipe.save()
        self.assertEquals(recipe.name, "Pancakes")
        self.assertEquals(recipe.ingredients, "Flour, Milk, Eggs, Sugar")

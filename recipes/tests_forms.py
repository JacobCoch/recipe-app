from django.test import TestCase
from .forms import RecipeForm, RecipeSearchForm
from .models import CustomUser as User


class RecipeFormTestCase(TestCase):
    def test_valid_form(self):
        data = {
            "name": "Spaghetti",
            "cooking_time": 30,
            "ingredients": "pasta, sauce, meat",
        }
        form = RecipeForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            "name": "",  # Name is required
            "cooking_time": 30,
            "ingredients": "pasta, sauce, meat",
        }
        form = RecipeForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_save(self):
        # Create a user
        user = User.objects.create_user(username="testuser", password="testpass")

        data = {
            "name": "Spaghetti",
            "cooking_time": 30,
            "ingredients": "pasta, sauce, meat",
        }
        form = RecipeForm(data=data)

        # Set the user as the author for the recipe
        form.instance.author = user

        self.assertTrue(form.is_valid())

        # Ensure the form can be saved
        recipe = form.save()
        self.assertEqual(recipe.name, "Spaghetti")
        self.assertEqual(recipe.cooking_time, 30)
        self.assertEqual(recipe.ingredients, "Pasta, Sauce, Meat")
        self.assertEqual(recipe.author, user)


class RecipeSearchFormTestCase(TestCase):
    def test_valid_form(self):
        data = {
            "recipe_name": "Spaghetti",
            "ingredients": "pasta, sauce, meat",
        }
        form = RecipeSearchForm(data=data)
        self.assertTrue(form.is_valid())

    def test_empty_form(self):
        # Both fields are not required, so an empty form is valid
        data = {}
        form = RecipeSearchForm(data=data)
        self.assertTrue(form.is_valid())

    def test_partial_form(self):
        # Either field can be empty
        data = {
            "recipe_name": "Spaghetti",
        }
        form = RecipeSearchForm(data=data)
        self.assertTrue(form.is_valid())

        data = {
            "ingredients": "pasta, sauce, meat",
        }
        form = RecipeSearchForm(data=data)
        self.assertTrue(form.is_valid())
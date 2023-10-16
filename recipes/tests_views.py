from django.test import TestCase
from django.urls import reverse
from .models import Recipe
from django.contrib.auth.models import User

class RecipeListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_recipe_list_view(self):
        response = self.client.get(reverse('recipes:recipes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes.html')

class RecipeDetailViewTest(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(
            name='Test Recipe',
            ingredients='Test Ingredients',
            cooking_time=10,
        )

    def test_recipe_detail_view(self):
        response = self.client.get(reverse('recipes:detail', args=[str(self.recipe.pk)]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/detail.html')
        self.assertContains(response, self.recipe.name)

    def test_context_data(self):
        response = self.client.get(reverse('detail', args=[str(self.recipe.pk)]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('difficulty' in response.context)
from django.test import TestCase
from django.urls import reverse
from .models import Recipe
from django.contrib.auth.models import User
from .views import RecipeDetailView


class RecipeListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_recipe_list_view(self):
        response = self.client.get(reverse("recipes:recipes"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipes.html")


class RecipeDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.recipe = Recipe.objects.create(
            name='Test Recipe',
            ingredients='ingr, ingr'    ,
            cooking_time=10,
        )

    def test_recipe_detail_view(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('recipes:detail', args=[self.recipe.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/detail.html')
        self.assertContains(response, self.recipe.name)
        self.assertContains(response, self.recipe.ingredients)
        self.assertContains(response, self.recipe.cooking_time)
        self.assertContains(response, self.recipe.calc_difficulty())

    def test_get_context_data(self):
        recipe = Recipe.objects.create(name="Test Recipe", ingredients="ingr, ingr", cooking_time=10)
        view = RecipeDetailView()
        view.object = recipe
        context = view.get_context_data()
        self.assertEqual(context["difficulty"], recipe.calc_difficulty())

    def test_calc_difficulty(self):
        # This test checks the calc_difficulty method of the Recipe model.
        # You can add more test cases based on the different difficulty levels.
        easy_recipe = Recipe.objects.create(
            name="Easy Recipe", ingredients="ingr, ingr, ingr", cooking_time=5
        )
        medium_recipe = Recipe.objects.create(
            name="Medium Recipe", ingredients="ingr, ingr, ingr, ingr, ingr", cooking_time=5
        )
        intermediate_recipe = Recipe.objects.create(
            name="Intermediate Recipe", ingredients="ingr, ingr, ingr", cooking_time=10
        )
        hard_recipe = Recipe.objects.create(
            name="Hard Recipe", ingredients="ingr, ingr, ingr, ingr", cooking_time=10
        )

        self.assertEqual(easy_recipe.calc_difficulty(), "Easy")
        self.assertEqual(medium_recipe.calc_difficulty(), "Medium")
        self.assertEqual(intermediate_recipe.calc_difficulty(), "Intermediate")
        self.assertEqual(hard_recipe.calc_difficulty(), "Hard")

    def test_detail_view_with_invalid_pk(self):
        # This test checks what happens when you access a detail view with an invalid primary key.
        url = reverse(
            "recipes:detail", args=[str(self.recipe.pk + 5)]
        )  # Adding 1 to the valid PK to make it invalid
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

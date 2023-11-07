from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import CustomUser as User
from .models import Recipe
from .views import AddRecipe, HomeView, Profile, RecipeDetailView


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("recipes:home")
        self.view = HomeView()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        # Create some sample recipes for testing
        self.recipe1 = Recipe.objects.create(
            name="Pasta",
            ingredients="flour, water, salt, eggs",
            cooking_time=20,
            author=self.user,
        )
        self.recipe2 = Recipe.objects.create(
            name="Pizza",
            ingredients="dough, tomato sauce, cheese",
            cooking_time=30,
            author=self.user,
        )
        # Create more sample recipes for the random suggestions
        for i in range(10):
            Recipe.objects.create(
                name=f"Recipe {i}",
                ingredients="ingredients",
                cooking_time=20,
                author=self.user,
            )

    def test_get_context_data(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/home.html")
        self.assertIn("random_suggestions", response.context)
        random_suggestions = response.context["random_suggestions"]
        # Ensure that there are 5 random suggestions
        self.assertEqual(len(random_suggestions), 5)
        # Ensure that the suggestions are instances of the Recipe model
        self.assertTrue(
            all(isinstance(recipe, Recipe) for recipe in random_suggestions)
        )


class RecipeListViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("recipes:recipe")
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        # Create some sample recipes for testing
        Recipe.objects.create(
            name="Pasta",
            ingredients="flour, water, salt, eggs",
            cooking_time=20,
            author_id=self.user.id,
        )
        Recipe.objects.create(
            name="Pizza",
            ingredients="dough, tomato sauce, cheese",
            cooking_time=30,
            author_id=self.user.id,
        )

    def test_get_context_data(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe.html")
        self.assertIn("recipes", response.context)
        self.assertIn("chart", response.context)
        self.assertEqual(len(response.context["recipes"]), 2)

    def test_post_valid_form(self):
        form_data = {
            "recipe_name": "Pasta",
            "ingredients": "flour, water, salt, eggs",
        }
        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe.html")
        self.assertIn("recipes", response.context)
        self.assertIn("chart", response.context)

    def test_post_invalid_form(self):
        # Test posting an invalid form
        form_data = {
            "recipe_name": "Pasta",
            "ingredients": "35",
        }
        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe.html")
        self.assertIn("recipes", response.context)
        self.assertIn("form", response.context)
        self.assertIn("chart", response.context)
        self.assertEqual(response.context["form"].is_valid(), True)


class RecipeDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            ingredients="ingr, ingr",
            cooking_time=10,
            author_id=self.user.id,
        )

    def test_recipe_detail_view(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("recipes:detail", args=[self.recipe.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/detail.html")
        self.assertContains(response, self.recipe.name)
        self.assertContains(response, self.recipe.ingredients)
        self.assertContains(response, self.recipe.cooking_time)
        self.assertContains(response, self.recipe.calc_difficulty())

    def test_get_context_data(self):
        recipe = Recipe.objects.create(
            name="Test Recipe",
            ingredients="ingr, ingr",
            cooking_time=10,
            author_id=self.user.id,
        )
        view = RecipeDetailView()
        view.object = recipe
        context = view.get_context_data()
        self.assertEqual(context["difficulty"], recipe.calc_difficulty())

    def test_detail_view_with_invalid_pk(self):
        # This test checks what happens when you access a detail view with an invalid primary key.
        url = reverse(
            "recipes:detail", args=[str(self.recipe.pk + 5)]
        )  # Adding 1 to the valid PK to make it invalid
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class AddRecipeTestCase(TestCase):
    def setUp(self):
        self.url = reverse("recipes:add")
        self.view = AddRecipe()
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_form_valid(self):
        self.client.login(username="testuser", password="testpass")
        form_data = {
            "name": "New Recipe",
            "ingredients": "Ingredient 1, Ingredient 2",
            "cooking_time": 30,
        }

        response = self.client.post(self.url, data=form_data)
        self.assertEqual(
            response.status_code, 302
        )  # 302 for a successful form submission
        self.assertEqual(Recipe.objects.count(), 1)
        new_recipe = Recipe.objects.first()
        self.assertEqual(new_recipe.name, "New Recipe")
        self.assertEqual(new_recipe.ingredients, "Ingredient 1, Ingredient 2")
        self.assertEqual(new_recipe.cooking_time, 30)
        self.assertEqual(new_recipe.author, self.user)

    def test_get_context_data(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/add_recipe.html")


class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            ingredients="Ingredient 1, Ingredient 2",
            cooking_time=30,
            author=self.user,
        )
        self.url = reverse("recipes:profile", kwargs={"username": self.user.username})
        self.view = Profile()

    def test_get_context_data(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/profile.html")
        self.assertIn("user", response.context)
        self.assertEqual(response.context["user"], self.user)
        self.assertIn("created_recipes", response.context)
        self.assertTrue(self.recipe in response.context["created_recipes"])


class DeleteRecipeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            ingredients="Ingredient 1, Ingredient 2",
            cooking_time=30,
            author=self.user,
        )
        self.url = reverse("recipes:delete_recipe", args=[self.recipe.pk])

    def test_delete_recipe_view_with_author(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(self.url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/detail.html")
        self.assertTrue(Recipe.objects.filter(pk=self.recipe.pk).exists())

    def test_delete_recipe_view_with_non_author(self):
        self.client.login(username="testuser2", password="testpass2")
        response = self.client.post(self.url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/login.html")
        self.assertTrue(Recipe.objects.filter(pk=self.recipe.pk).exists())

    def test_delete_recipe_view_get_request(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(self.url, follow=True)  # Change GET to POST

        self.assertEqual(response.status_code, 200)  # Check the status code
        self.assertTemplateUsed(
            response, "recipes/detail.html"
        )  # Use the appropriate template
        self.assertTrue(Recipe.objects.filter(pk=self.recipe.pk).exists())


class EditRecipeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            ingredients="Ingredient 1, Ingredient 2",
            cooking_time=30,
            author=self.user,
        )
        self.url = reverse("recipes:edit_recipe", args=[self.recipe.pk])

    def test_edit_recipe_view_with_author(self):
        self.client.login(username="testuser", password="testpass")
        new_name = "Updated Recipe Name"
        new_ingredients = "Updated Ingredient 1, Updated Ingredient 2"
        new_cooking_time = 45

        response = self.client.post(
            self.url,
            data={
                "name": new_name,
                "ingredients": new_ingredients,
                "cooking_time": new_cooking_time,
            },
        )

        self.assertEqual(response.status_code, 302)  # Check the redirect status code
        updated_recipe = Recipe.objects.get(pk=self.recipe.pk)
        self.assertEqual(updated_recipe.name, new_name)  # Check if the name is updated
        self.assertEqual(
            updated_recipe.ingredients, new_ingredients
        )  # Check if the ingredients are updated
        self.assertEqual(
            updated_recipe.cooking_time, new_cooking_time
        )  # Check if the cooking time is updated

    def test_edit_recipe_view_with_non_author(self):
        self.client.login(username="testuser2", password="testpass2")
        new_name = "Updated Recipe Name"
        new_ingredients = "Updated Ingredient 1, Updated Ingredient 2"
        new_cooking_time = 45

        response = self.client.post(
            self.url,
            data={
                "name": new_name,
                "ingredients": new_ingredients,
                "cooking_time": new_cooking_time,
            },
        )

        self.assertEqual(response.status_code, 302)  # Check the redirect status code
        updated_recipe = Recipe.objects.get(pk=self.recipe.pk)
        self.assertNotEqual(
            updated_recipe.name, new_name
        )  # Check if the name is not updated
        self.assertNotEqual(
            updated_recipe.ingredients, new_ingredients
        )  # Check if the ingredients are not updated
        self.assertNotEqual(updated_recipe.cooking_time, new_cooking_time)


class FavedRecipeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            ingredients="Ingredient 1, Ingredient 2",
            cooking_time=30,
            author=self.user,
        )
        self.url = reverse("recipes:faved_recipe", args=[self.recipe.pk])

    def test_faved_recipe_view_add_favorite(self):
        self.client.login(username="testuser", password="testpass")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)  # Check the response status code
        user = User.objects.get(username="testuser")
        self.assertTrue(
            user.fav_recipes.filter(pk=self.recipe.pk).exists()
        )  # Check if the recipe is favorited

    def test_faved_recipe_view_remove_favorite(self):
        self.client.login(username="testuser", password="testpass")
        self.user.fav_recipes.add(self.recipe)  # Add the recipe to favorites

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)  # Check the response status code
        user = User.objects.get(username="testuser")
        self.assertFalse(
            user.fav_recipes.filter(pk=self.recipe.pk).exists()
        )  # Check if the recipe is unfavorited


class UpdateProfilePictureTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.url = reverse(
            "recipes:update_profile_picture", kwargs={"username": self.user.username}
        )
        self.image = SimpleUploadedFile(
            "profile_pics/profile.jpg",
            content=b"file_content",
            content_type="image/jpeg",
        )

    def test_update_profile_picture(self):
        self.client.login(username="testuser", password="testpass")

        response = self.client.post(self.url, {"profile_pic": self.image})

        self.assertEqual(response.status_code, 302)
        updated_user = User.objects.get(username="testuser")
        self.assertIsNotNone(updated_user.pic)

    def test_update_profile_picture_with_non_author(self):
        self.client.login(username="testuser2", password="testpass2")

        response = self.client.post(self.url, {"profile_pic": self.image})

        self.assertEqual(response.status_code, 302)
        updated_user = User.objects.get(username="testuser")
        self.assertIsNotNone(updated_user.pic)

from django.test import TestCase
from django.urls import reverse
from .models import Recipe, CustomUser


# Create your tests here.
class RecipeModelTest(TestCase):
    def setUpTestData():
        CustomUser.objects.create(id=1, username="testuser", password="testpass")
        Recipe.objects.create(
            name="Pasta", ingredients="flour, water, salt, eggs", cooking_time=10, author_id=1
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

    def test_get_absolute_url(self):
        recipe = Recipe.objects.get(id=1)
        expected_url = reverse("recipes:detail", kwargs={"pk": 1})
        self.assertEquals(recipe.get_absolute_url(), expected_url)

    def test_fav_recipes_field(self):
        recipe = Recipe.objects.get(id=1)
        user = CustomUser.objects.get(id=1)
        user.fav_recipes.add(recipe)
        self.assertEquals(user.fav_recipes.count(), 1)


class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpass"
        )

    def test_user_creation(self):
        self.assertTrue(self.user.check_password("testpass"))

    def test_user_str(self):
        self.assertEqual(str(self.user), "testuser")

    def test_user_get_absolute_url(self):
        expected_url = reverse("recipes:profile", kwargs={"username": self.user.username})
        self.assertEqual(self.user.get_absolute_url(), expected_url)

    def test_user_bio_field(self):
        self.user.bio = "this is a test bio"
        self.assertEqual(self.user.bio, "this is a test bio")

    def test_user_pic_field(self):
        self.user.pic = "profile_pics/test.jpg"
        self.assertEqual(self.user.pic, "profile_pics/test.jpg")    

    
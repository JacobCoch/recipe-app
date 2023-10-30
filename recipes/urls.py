from django.urls import path
from .views import RecipeListView, RecipeDetailView, HomeView, AddRecipe, Profile
from . import views

app_name = "recipes"

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("recipe/", RecipeListView.as_view(), name="recipe"),
    path("recipe/<int:pk>/", RecipeDetailView.as_view(), name="detail"),
    path("recipe/add/", AddRecipe.as_view(), name="add"),
    path("recipe/<int:recipe_id>/delete/", views.delete_recipe, name="delete_recipe"),
    path("fav/<int:recipe_id>/", views.faved_recipe, name="faved_recipe"),
    path("profile/<slug:username>/", Profile.as_view(), name="profile"),
]

from django.urls import path
from .views import RecipeListView, RecipeDetailView, HomeView, AddRecipe


app_name = "recipes"

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("recipe/", RecipeListView.as_view(), name="recipe"),
    path("recipe/<int:pk>/", RecipeDetailView.as_view(), name="detail"),
    path("recipe/add/", AddRecipe.as_view(), name="add")
]

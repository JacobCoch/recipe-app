from django.urls import path
from .views import RecipeListView, RecipeDetailView


app_name = "recipes"

urlpatterns = [
    path("recipe/", RecipeListView.as_view(), name="recipes"),
    path("recipe/<int:pk>/", RecipeDetailView.as_view(), name="detail"),
]

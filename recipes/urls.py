from django.urls import path
from .views import home, RecipeListView, RecipeDetailView

app_name = 'recipes'

urlpatterns = [
  path('', home),
  path('recipe/', RecipeListView.as_view(), name='list'),
  path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='detail')
]
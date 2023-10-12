from django.urls import path
from .views import RecipeListView, RecipeDetailView, home
from django.views.generic import RedirectView

app_name = 'recipes'

urlpatterns = [
  path('', home),
  path('recipe/', RecipeListView.as_view(),  name='home'),
  path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='detail')
]
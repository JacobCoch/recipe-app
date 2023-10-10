from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Recipe

# Create your views here.
def home(request):
  return render(request, 'recipes/home.html')

class RecipeListView(ListView):
  model = Recipe
  template_name = 'recipes/main.html'

class RecipeDetailView(DetailView):
  model = Recipe
  template_name = 'recipes/detail.html'

  def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.object
        difficulty = recipe.calc_difficulty()  
        context['difficulty'] = difficulty
        return context
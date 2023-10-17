from django.views.generic import DetailView, ListView
from .models import Recipe
from django.contrib.auth.mixins import LoginRequiredMixin


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipes/recipes.html"


class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = "recipes/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.object
        difficulty = recipe.calc_difficulty()
        context["difficulty"] = difficulty
        return context

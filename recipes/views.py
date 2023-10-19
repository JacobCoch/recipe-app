from django.views.generic import DetailView, ListView
from .models import Recipe
from django.contrib.auth.mixins import LoginRequiredMixin
import random
import logging

class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipes/recipes.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_recipes = Recipe.objects.all()

        
        random_recipes = random.sample(list(all_recipes), 3)

        
        context["random_suggestions"] = random_recipes


        return context

class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = "recipes/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.object
        difficulty = recipe.calc_difficulty()
        context["difficulty"] = difficulty
        return context

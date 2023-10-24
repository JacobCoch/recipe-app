from .utils import get_chart
from django.views.generic import DetailView, ListView, CreateView

from .models import Recipe
from .forms import RecipeForm
from django.contrib.auth.mixins import LoginRequiredMixin
import matplotlib
import pandas as pd
import random
import logging


class HomeView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipes/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_recipes = Recipe.objects.all()
        random_recipes = random.sample(list(all_recipes), 5)

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


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipes/recipe.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
         
        all_recipes = Recipe.objects.all()
        context["recipes"] = all_recipes
        return context

class AddRecipe(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = "recipes/add_recipe.html"
    form_class = RecipeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
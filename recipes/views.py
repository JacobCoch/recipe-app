from django.shortcuts import  redirect, get_object_or_404
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

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
    

def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.user == recipe.author:
        if request.method == "POST":
            recipe.delete()
            return redirect("recipes:recipe")
    else:
        # Handle cases where the user is not the author (you can redirect or show an error)
        pass
    return redirect("recipes:recipe")
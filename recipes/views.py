from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView
from .models import Recipe
from .utils import render_chart
from django.contrib.auth.models import User

from .forms import RecipeForm, FavoriteRecipeForm, RecipeSearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

import pandas as pd

import random



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
    form = RecipeSearchForm()
    chart = None

    def post(self, request, *args, **kwargs):
        form = RecipeSearchForm(self.request.POST)
        
        if form.is_valid():
            recipe_name = form.cleaned_data["recipe_name"]
            ingredients = form.cleaned_data["ingredients"]
            print(recipe_name, ingredients)

        
            if recipe_name:
                recipes = Recipe.objects.filter(name__icontains=recipe_name)
            elif ingredients:
                recipes = Recipe.objects.filter(ingredients__icontains=ingredients)
            else:
                recipes = Recipe.objects.all()

            context = {
                "recipes": recipes,
                "form": form,

            }

            return render(self.request, "recipes/recipe.html", context)
        

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


@login_required
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


@login_required
def faved_recipe(request, recipe_id):
    if request.method == "POST":
        form = FavoriteRecipeForm(request.POST)
        if form.is_valid():
            recipe_id = form.cleaned_data("recipe_id")
            user = request.user
            recipe = Recipe.objects.get(pk=recipe_id)

            if recipe.users_favorite.filter(pk=user.pk).exists():
                recipe.users_favorite.remove(user)
            else:
                recipe.users_favorite.add(user)
        return redirect("recipes:detail", pk=recipe_id)


class Profile(LoginRequiredMixin, DetailView):
    model = User
    template_name = "recipes/profile.html"
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username"

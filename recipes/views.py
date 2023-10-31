from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView
from .models import Recipe
from django.db.models import Q
from django.contrib.auth.models import User
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
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


class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/recipe.html"
    form = RecipeSearchForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_recipes = Recipe.objects.all()
        context["recipes"] = all_recipes

        # Generate the graph here
        x = [recipe.name for recipe in all_recipes]
        y = [recipe.cooking_time for recipe in all_recipes]
        chart = self.get_plot(x, y)
        context["chart"] = chart

        return context

    def get_plot(self, x, y):
        buffer = BytesIO()
        plt.switch_backend('AGG')
        plt.figure(figsize=(10, 5))
        plt.title('recipe chart')
        plt.plot(x, y)
        plt.xticks(rotation=45)
        plt.xlabel('recipe')
        plt.ylabel('cooking time')
        plt.tight_layout()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        graph = base64.b64encode(image_png).decode('utf-8')
        buffer.close()
        return graph

    def post(self, request, *args, **kwargs):
        form = RecipeSearchForm(self.request.POST)

        if form.is_valid():
            recipe_name = form.cleaned_data["recipe_name"]
            ingredients = form.cleaned_data["ingredients"]

            recipes = Recipe.objects.all()

            if recipe_name:
                recipes = recipes.filter(Q(name__icontains=recipe_name))

            if ingredients:
                recipes = recipes.filter(Q(ingredients__icontains=ingredients))

            context = {
                "recipes": recipes,
                "form": form,
            }

            # Update the graph based on the filtered recipes
            x = [recipe.name for recipe in recipes]
            y = [recipe.cooking_time for recipe in recipes]
            chart = self.get_plot(x, y)
            context["chart"] = chart

            return render(self.request, "recipes/recipe.html", context)

    def graph_view(request):
        # You can access the chart within the context here
        chart = request.context["chart"]
        return render(request, 'recipes/recipe.html', {'chart': chart})


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

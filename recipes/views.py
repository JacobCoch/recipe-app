import base64
from io import BytesIO

import matplotlib
import matplotlib.pyplot as plt
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, ListView

from .models import Recipe

matplotlib.use("Agg")
import random

import pandas as pd
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import FavoriteRecipeForm, RecipeForm, RecipeSearchForm


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
        plt.switch_backend("AGG")
        plt.figure(figsize=(10, 5))
        plt.title("Recipe Chart")
        plt.bar(x, y)
        plt.xticks(rotation=45)
        plt.xlabel("Recipes")
        plt.ylabel("Cooking Time")
        plt.tight_layout()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_png = buffer.getvalue()
        graph = base64.b64encode(image_png).decode("utf-8")
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

            if not recipe_name and not ingredients:
                recipes = Recipe.objects.all()

            context = {
                "recipes": recipes,
                "form": form,
            }

            if not recipes:
                messages.info(self.request, "No recipes found")

            # Update the graph based on the filtered recipes
            x = [recipe.name for recipe in recipes]
            y = [recipe.cooking_time for recipe in recipes]
            chart = self.get_plot(x, y)
            context["chart"] = chart

            return render(self.request, "recipes/recipe.html", context)

    def graph_view(request):
        # You can access the chart within the context here
        chart = request.context["chart"]
        return render(request, "recipes/recipe.html", {"chart": chart})


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
            # Check for a confirmation parameter sent via POST
            confirmation = request.POST.get("confirmation")

            if confirmation == "yes":
                # User has confirmed the deletion
                recipe.delete()
                messages.success(request, "Recipe deleted successfully.")
                return redirect("recipes:recipe")
            else:
                # User canceled the deletion
                messages.info(request, "Recipe deletion canceled.")
                return redirect("recipes:recipe")
    return redirect("recipes:recipe")


@login_required
def edit_recipe(request,recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.user == recipe.author:
        if request.method == "POST":
            recipe_form = RecipeForm(request.POST, instance=recipe)
            if recipe_form.is_valid():
                recipe_form.save()
                return redirect("recipes:detail", pk=recipe_id)
    else:
        pass
    return redirect("recipes:detail", pk=recipe_id)


@login_required
def faved_recipe(request, recipe_id):
    user = request.user
    recipe = Recipe.objects.get(pk=recipe_id)
    recipe_favorites = recipe.users_favorite.all()

    context = {
        "recipe": recipe,
        "recipe_favorites": recipe_favorites,
    }
    
    return render("recipes/profile.html", context, pk=recipe_id)
   
    


class Profile(LoginRequiredMixin, DetailView):
    model = User
    template_name = "recipes/profile.html"
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username"

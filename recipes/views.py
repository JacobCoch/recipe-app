from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView
from .models import Recipe
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from .forms import RecipeForm, FavoriteRecipeForm, RecipeSearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd
from django.db.models import Q
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


def search(request):
    template_name = "recipes/recipe.html"
    form = RecipeSearchForm(request.POST or None)

    if request.method == "POST":
        recipe_name = request.POST.get("recipe_name")
        ingredients = request.POST.get("ingredients")
        chart_type = request.POST.get("chart_type")
        print(recipe_name, ingredients, chart_type)

        # You can store the search parameters in session or cookies if needed
        request.session['search_params'] = {
            'recipe_name': recipe_name,
            'ingredients': ingredients,
            'chart_type': chart_type,
        }

        # Redirect to the RecipeListView to display the filtered results
        return redirect('recipe')

    context = {"form": form}
    return render(request, template_name, context)

class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipes/recipe.html"

    def get_queryset(self):
        # Retrieve search parameters from session or cookies
        search_params = self.request.session.get('search_params', {})
        recipe_name = search_params.get('recipe_name')
        ingredients = search_params.get('ingredients')
        chart_type = search_params.get('chart_type')

        # Filter the recipes based on search parameters
        queryset = Recipe.objects.all()
        if recipe_name:
            queryset = queryset.filter(name__icontains=recipe_name)
        if ingredients:
            queryset = queryset.filter(ingredients__icontains=ingredients)
        # Add more filters as needed

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_recipes = Recipe.objects.all()
        context["recipes"] = all_recipes
        return context


"""
def render_chart(request, chart_type, data, **kwargs):
    plt.switch_backend("AGG")
    fig = plt.figure(figsize=(12, 8), dpi=100)
    ax = fig.add_subplot(111)

    if chart_type == "#1":
        plt.title("Cooking Time by Recipe", fontsize=20)
        plt.bar(data["title"], data["cooking_time"])
        plt.xlabel("Recipes", fontsize=16)
        plt.ylabel("Cooking Time (min)", fontsize=16)
    elif chart_type == "#2":
        plt.title("Recipes Cooking Time Comparison", fontsize=20)
        labels = kwargs.get("labels")
        plt.pie(data["cooking_time"], labels=None, autopct="%1.1f%%")
        plt.legend(
            data["title"],
            loc="upper right",
            bbox_to_anchor=(1.0, 1.0),
            fontsize=12,
        )
    elif chart_type == "#3":
        plt.title("Cooking Time by Recipe", fontsize=20)
        x_values = data["title"].to_numpy()
        y_values = data["cooking_time"].to_numpy()
        plt.plot(x_values, y_values)
        plt.xlabel("Recipes", fontsize=16)
        plt.ylabel("Cooking Time (min)", fontsize=16)
    else:
        print("Unknown chart type.")

    plt.tight_layout(pad=3.0)

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    chart_image = base64.b64encode(buffer.read()).decode("utf-8")

    return chart_image
"""


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

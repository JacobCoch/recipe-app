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


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipes/recipe.html"
    form = RecipeSearchForm()

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

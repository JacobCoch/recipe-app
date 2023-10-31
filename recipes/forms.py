from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["name", "cooking_time", "pic", "ingredients"]


class RecipeSearchForm(forms.Form):
    recipe_name = forms.CharField(
        label="Recipe Name",
        max_length=100,
        required=False,
    )
    ingredients = forms.CharField(
        label="Ingredients (separated by commas)",
        max_length=100,
        required=False,
    )


class FavoriteRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            []
        )  # This can be an empty list, as you don't need any fields from the Recipe model

    recipe_id = forms.IntegerField(widget=forms.HiddenInput())

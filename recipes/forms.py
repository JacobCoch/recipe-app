from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'cooking_time', 'pic', 'ingredients']


CHART_CHOICES = (
    ('#1', 'Pie Chart'),
    ('#2', 'Bar Chart'),
    ('#3', 'Line Chart')
)
class RecipeSearchForm(forms.Form):
    recipe_name = forms.CharField(max_length=100, required=False)
    ingredients = forms.CharField(max_length=100, required=False)
    chart_type = forms.ChoiceField(choices=CHART_CHOICES, required=False)

class FavoriteRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = []  # This can be an empty list, as you don't need any fields from the Recipe model

    recipe_id = forms.IntegerField(widget=forms.HiddenInput())
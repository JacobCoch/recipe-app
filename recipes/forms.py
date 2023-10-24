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

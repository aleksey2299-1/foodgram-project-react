from django import forms
from django.forms import ModelForm

from recipes.models import Recipe


class RecipeAdminForm(ModelForm):
    in_favorites = forms.IntegerField(label="В избранном", disabled=True)

    class Meta:
        model = Recipe
        fields = ['name', 'in_favorites', 'cooking_time', 'author',
                  'text', 'image']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        initial = {}
        if instance:
            initial = {
                "in_favorites": instance.in_favorites_count(),
            }
            super().__init__(*args, **kwargs, initial=initial)
        else:
            super().__init__(*args, **kwargs)

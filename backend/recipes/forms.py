from django import forms

from recipes.models import Recipe
from users.models import CustomBaseUser


class RecipeAdminForm(forms.ModelForm):
    in_favorites = forms.IntegerField(label="В избранном",
                                      disabled=True, required=False)

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


class FavoriteThroughForm(forms.ModelForm):
    recipe = forms.ModelChoiceField(queryset=Recipe.objects.all(),
                                    label='Рецепт', required=True)
    custombaseuser = forms.ModelChoiceField(
        queryset=CustomBaseUser.objects.all(),
        label='Пользователь',
        required=True,
    )

    class Meta:
        model = Recipe.added_to_favorites.through
        fields = ('recipe', 'custombaseuser')


class ShoppingCartThroughForm(forms.ModelForm):
    recipe = forms.ModelChoiceField(queryset=Recipe.objects.all(),
                                    label='Рецепт', required=True)
    custombaseuser = forms.ModelChoiceField(
        queryset=CustomBaseUser.objects.all(),
        label='Пользователь',
        required=True,
    )

    class Meta:
        model = Recipe.shopping_cart.through
        fields = ('recipe', 'custombaseuser')

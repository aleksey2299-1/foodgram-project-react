from django_filters import NumberFilter, FilterSet, ModelMultipleChoiceFilter

from recipes.models import Recipe, Tag


class RecipeFilter(FilterSet):
    author = NumberFilter(field_name='author__id')
    is_favorited = NumberFilter(field_name='added_to_favorites',
                                method='filter_favorite')
    is_in_shopping_cart = NumberFilter(field_name='shopping_cart',
                                       method='filter_cart')
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    def filter_favorite(self, queryset, name, value):
        if value == 1:
            return queryset.filter(
                added_to_favorites__email=self.request.user.email
            )
        elif value == 0:
            return queryset.exclude(
                added_to_favorites__email=self.request.user.email
            )

    def filter_cart(self, queryset, name, value):
        if value == 1:
            return queryset.filter(
                shopping_cart__email=self.request.user.email
            )
        elif value == 0:
            return queryset.exclude(
                shopping_cart__email=self.request.user.email
            )

    class Meta:
        model = Recipe
        fields = []

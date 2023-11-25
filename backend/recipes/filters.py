from django_filters import NumberFilter, FilterSet, ModelMultipleChoiceFilter, MultipleChoiceFilter

from recipes.models import Recipe, Tag

CHOICES = ((0, False), (1, True))


class RecipeFilter(FilterSet):
    author = NumberFilter(field_name='author__id')
    is_favorited = MultipleChoiceFilter(
        field_name='added_to_favorites',
        method='filter_favorite',
        choices=CHOICES,
    )
    is_in_shopping_cart = MultipleChoiceFilter(
        field_name='shopping_cart', method='filter_cart', choices=CHOICES,
    )
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    def filter_favorite(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return queryset
        if value == ['1']:
            return queryset.filter(
                added_to_favorites__email=self.request.user.email
            )
        else:
            return queryset.exclude(
                added_to_favorites__email=self.request.user.email
            )

    def filter_cart(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return queryset
        if value == ['1']:
            return queryset.filter(
                shopping_cart__email=self.request.user.email
            )
        else:
            return queryset.exclude(
                shopping_cart__email=self.request.user.email
            )

    class Meta:
        model = Recipe
        fields = []

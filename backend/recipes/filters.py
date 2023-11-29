from django_filters import (AllValuesMultipleFilter, FilterSet,
                            MultipleChoiceFilter)

from recipes.models import Recipe

CHOICES = ((0, False), (1, True))


class RecipeFilter(FilterSet):
    is_favorited = MultipleChoiceFilter(
        field_name='added_to_favorites',
        method='filter_by_field',
        choices=CHOICES,
    )
    is_in_shopping_cart = MultipleChoiceFilter(
        field_name='shopping_cart', method='filter_by_field', choices=CHOICES,
    )
    tags = AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ['author', 'is_favorited', 'is_in_shopping_cart', 'tags']

    def filter_by_field(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return queryset
        email_filter = '__'.join([name, 'email'])
        if value == ['1']:
            return queryset.filter(**{email_filter: self.request.user.email})
        else:
            return queryset.exclude(**{email_filter: self.request.user.email})

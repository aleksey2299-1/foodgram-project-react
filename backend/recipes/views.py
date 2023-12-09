from io import StringIO

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.filters import RecipeFilter
from recipes.models import Ingredient, Recipe, Tag
from recipes.paginators import RecipePagination
from recipes.permissions import AuthorPermission
from recipes.serializers import (IngredientSerializer, RecipeCreateSerializer,
                                 RecipeFavoriteSerializer, RecipeSerializer,
                                 TagSerializer)


def post_method(field_name, request, pk):
    user = request.user
    try:
        recipe = Recipe.objects.get(id=pk)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    check = getattr(recipe, field_name).filter(email=user.email).exists()
    if not check:
        getattr(recipe, field_name).add(user)
        serializer = RecipeFavoriteSerializer(
            recipe,
            context={"request": request},
        )
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def delete_method(field_name, request, pk):
    user = request.user
    try:
        recipe = Recipe.objects.get(id=pk)
    except Exception:
        return Response(status=status.HTTP_404_NOT_FOUND)
    check = getattr(recipe, field_name).filter(email=user.email).exists()
    if check:
        getattr(recipe, field_name).remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = RecipePagination
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeCreateSerializer
        return RecipeSerializer

    def get_permissions(self):
        if self.action in ('partial_update', 'destroy'):
            return (AuthorPermission(),)
        return super().get_permissions()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = False
        return super().update(request, *args, **kwargs)

    @action(
        methods=["post"], detail=True, url_path='favorite',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def favorite(self, request, pk):
        field_name = 'added_to_favorites'
        return post_method(field_name, request, pk)

    @favorite.mapping.delete
    def favorite_delete(self, request, pk):
        field_name = 'added_to_favorites'
        return delete_method(field_name, request, pk)

    @action(
        methods=["post"], detail=True, url_path='shopping_cart',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def shopping_cart(self, request, pk):
        field_name = 'shopping_cart'
        return post_method(field_name, request, pk)

    @shopping_cart.mapping.delete
    def shopping_cart_delete(self, request, pk):
        field_name = 'shopping_cart'
        return delete_method(field_name, request, pk)

    @action(
        methods=["get"], url_path='download_shopping_cart', detail=False,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        shop_dict = {}
        user = request.user
        recipes = user.shopping_cart.all()
        for recipe in recipes:
            for ingredient in recipe.ingredients.all():
                name = ingredient.ingredient.name.capitalize()
                measurement_unit = ingredient.ingredient.measurement_unit
                full_ingredient = name + ' (' + measurement_unit + ') - '
                amount = ingredient.amount
                shop_dict[full_ingredient] = (
                    shop_dict.get(full_ingredient, 0) + amount
                )
        shopping_cart = StringIO()
        for key, value in shop_dict.items():
            shopping_cart.write(key + str(value) + '\n')
        filename = 'shopping_cart.txt'
        response = HttpResponse(shopping_cart.getvalue(),
                                content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename={0}'.format(filename)
        )
        return response


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ('get',)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    http_method_names = ('get',)
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = {'name': ['icontains']}

from io import StringIO

from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse

from recipes.filters import RecipeFilter
from recipes.models import Recipe, Tag, Ingredient
from recipes.serializers import (
    RecipeSerializer,
    TagSerializer,
    IngredientSerializer,
    RecipeFavoriteSerializer,
    RecipeCreateSerializer,
)
from recipes.paginators import RecipePagination
from recipes.permissions import AuthorPermission


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
        if self.action == 'create' or self.action == 'partial_update':
            return RecipeCreateSerializer
        return RecipeSerializer

    def get_permissions(self):
        if self.action == 'partial_update' or self.action == 'destroy':
            return (AuthorPermission(),)
        return super().get_permissions()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = False
        return super().update(request, *args, **kwargs)

    @action(
        methods=["post", "delete"], detail=True, url_path='favorite',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def favorite(self, request, pk):
        user = request.user
        if request.method == 'POST':
            try:
                recipe = Recipe.objects.get(id=pk)
            except Exception:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            check = recipe.added_to_favorites.filter(email=user.email).exists()
            if not check:
                recipe.added_to_favorites.add(user)
                serializer = RecipeFavoriteSerializer(
                    recipe,
                    context={"request": request},
                )
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            try:
                recipe = Recipe.objects.get(id=pk)
            except Exception:
                return Response(status=status.HTTP_404_NOT_FOUND)
            check = recipe.added_to_favorites.filter(email=user.email).exists()
            if check:
                recipe.added_to_favorites.remove(user)
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["post", "delete"], detail=True, url_path='shopping_cart',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def shopping_cart(self, request, pk):
        user = request.user
        if request.method == 'POST':
            try:
                recipe = Recipe.objects.get(id=pk)
            except Exception:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            check = recipe.shopping_cart.filter(email=user.email).exists()
            if not check:
                recipe.shopping_cart.add(user)
                serializer = RecipeFavoriteSerializer(
                    recipe,
                    context={"request": request},
                )
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            try:
                recipe = Recipe.objects.get(id=pk)
            except Exception:
                return Response(status=status.HTTP_404_NOT_FOUND)
            check = recipe.shopping_cart.filter(email=user.email).exists()
            if check:
                recipe.shopping_cart.remove(user)
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)

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
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)
    # filterset_fields = {'name': ['istartswith']} # нечувствительно к регистру

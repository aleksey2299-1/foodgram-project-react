from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from recipes.filters import RecipeFilter
from recipes.models import Recipe, Tag, Ingredient
from recipes.serializers import (
    RecipeSerializer,
    TagSerializer,
    IngredientSerializer,
    RecipeFavoriteSerializer,
    RecipeListSerializer,
)
from recipes.paginators import RecipePagination


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = RecipePagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeListSerializer
        return RecipeSerializer

    @action(
        methods=["post", "delete"], detail=True, url_path='favorite',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def favorite(self, request, pk):
        user = request.user
        try:
            recipe = Recipe.objects.get(id=pk)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        check = recipe.added_to_favorites.filter(email=user.email).exists()
        if request.method == 'POST':
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
        try:
            recipe = Recipe.objects.get(id=pk)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        check = recipe.shopping_cart.filter(email=user.email).exists()
        if request.method == 'POST':
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
            if check:
                recipe.shopping_cart.remove(user)
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ('get',)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    http_method_names = ('get',)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = {'name': ['istartswith']}  # нечувствительно к регистру

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from recipes.fields import Base64ImageField
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from users.models import CustomBaseUser

ru_error_messages = {
    'does_not_exist': _('Недопустимый первичный ключ "{pk_value}"'
                        ' - объект не существует.'),
}


def create_ingredients(data, model):
    for ingredient in data:
        IngredientRecipe.objects.create(
            amount=ingredient['amount'],
            ingredient=ingredient['id'],
            recipe=model,
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        error_messages=ru_error_messages,
    )

    class Meta:
        model = IngredientRecipe
        fields = ('amount', 'id',)


class RecipeFavoriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeSerializer(many=True, allow_empty=False)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        allow_empty=False,
        error_messages=ru_error_messages,
    )
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image', 'name',
                  'text', 'cooking_time',)

    def validate_ingredients(self, value):
        set_for_dict = set()
        set_for_dict = set_for_dict.union(x['id'] for x in value)
        if len(set_for_dict) < len(value):
            raise serializers.ValidationError(
                "Повторяющиеся данные."
            )
        return value

    def validate_tags(self, value):
        if len(set(value)) < len(value):
            raise serializers.ValidationError(
                "Повторяющиеся данные."
            )
        return value

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        ingredients_data = sorted(ingredients_data, key=lambda d: d['id'].name)
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        create_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        ingredients_data = sorted(ingredients_data, key=lambda d: d['id'].name)
        instance.ingredients.filter(recipe=instance).delete()
        create_ingredients(ingredients_data, instance)
        instance = super().update(instance, validated_data)
        instance.save()
        return instance

    def to_representation(self, instance):
        serializer = RecipeSerializer(instance, context={
            'request': self.context['request']
        })
        return serializer.data


class IngredientRecipeListSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomBaseUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeListSerializer(many=True)
    tags = TagSerializer(many=True)
    image = Base64ImageField(required=False, allow_null=True)
    author = AuthorSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        if not self.context['request'].user.is_anonymous:
            return obj.added_to_favorites.filter(
                email=self.context['request'].user.email).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        if not self.context['request'].user.is_anonymous:
            return obj.shopping_cart.filter(
                email=self.context['request'].user.email).exists()
        return False

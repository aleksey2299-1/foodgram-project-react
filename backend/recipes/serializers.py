import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import Recipe, Tag, Ingredient, IngredientRecipe
from users.models import CustomBaseUser


def validate_ingredients(value):
    print(value[0], len(value))
    for i in range(len(value)):
        for j in range(i + 1, len(value)):
            print(i, j)
            if value[i] == value[j]:
                print('True')
                return serializers.ValidationError(
                    "Similar ingredients input"
                    )
    return value


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

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
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True, allow_empty=False)
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image', 'name',
                  'text', 'cooking_time',)

    def validate_ingredients(self, value):
        if len(value) > 1:
            for i in range(len(value)):
                for j in range(i + 1, len(value)):
                    if value[i] == value[j]:
                        raise serializers.ValidationError(
                            "Similar ingredients input"
                            )
        return value

    def validate_tags(self, value):
        if len(value) > 1:
            for i in range(len(value)):
                for j in range(i + 1, len(value)):
                    if value[i] == value[j]:
                        raise serializers.ValidationError(
                            "Similar tags input"
                            )
        return value

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient_data in ingredients_data:
            IngredientRecipe.objects.create(
                amount=ingredient_data['amount'],
                ingredient=ingredient_data['id'],
                recipe=recipe,
            )
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        instance.ingredients.filter(recipe=instance).delete()
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                amount=ingredient['amount'],
                ingredient=ingredient['id'],
                recipe=instance,
            )
        instance = super().update(instance, validated_data)
        instance.save()
        return instance

    # def __init__(self, *args, **kwargs):
    #     remove_fields = kwargs.pop('remove_fields', None)
    #     super(RecipeCreateSerializer, self).__init__(*args, **kwargs)

    #     if remove_fields:
    #         for field_name in remove_fields:
    #             self.fields.pop(field_name)

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

    # def __init__(self, *args, **kwargs):
    #     if kwargs['context']['request'].user.is_anonymous:
    #         del self.fields['is_favorited']
    #         del self.fields['is_in_shopping_cart']
    #     super().__init__(*args, **kwargs)

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

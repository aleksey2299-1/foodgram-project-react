from rest_framework import serializers

from .models import Recipe, Tag, Ingridient, User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'slug')


class IngridientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingridient
        fields = ('name', 'amount', 'measurement')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class RecipeSerializer(serializers.ModelSerializer):
    recipe_tag = TagSerializer(many=True)
    recipe_ingridients = IngridientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('author', 'name', 'tag', 'time', 'desc', 'ingridient')

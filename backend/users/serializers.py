from rest_framework import serializers

from recipes.serializers import RecipeSerializer
from users.models import CustomBaseUser


class UserForAnonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomBaseUser
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name')


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomBaseUser
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        return self.context['request'].user.subscribe.filter(
            email=obj.email
        ).exists()


class UserSubscribeSerializer(UserSerializer):
    recipes = RecipeSerializer(
        remove_fields=['tags', 'ingredients', 'text', 'author'],
        many=True,
        read_only=True,
    )
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomBaseUser
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return obj.recipes.count()

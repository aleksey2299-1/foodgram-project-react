from django.core.paginator import Paginator
from rest_framework import serializers

from recipes.models import Recipe
from recipes.serializers import Base64ImageField
from users.models import CustomBaseUser


class UserForAnonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomBaseUser
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 4}}

    def create(self, validated_data):
        user = CustomBaseUser(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        return super().update(instance, validated_data)


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


class UserRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserSubscribeSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField('paginated_recipes')
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomBaseUser
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def paginated_recipes(self, obj):
        if self.context['request'].query_params.get('recipes_limit'):
            recipes_limit = self.context['request'].query_params.get(
                'recipes_limit',
            )
            paginator = Paginator(obj.recipes.all(), recipes_limit)
            recipes = paginator.page(1)
        else:
            recipes = obj.recipes.all()
        serializer = UserRecipeSerializer(recipes, many=True, read_only=True)
        return serializer.data

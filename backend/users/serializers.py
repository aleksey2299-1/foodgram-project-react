from rest_framework import serializers

from recipes.serializers import RecipeSerializer
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











# def __init__(self, *args, **kwargs):
#         # Don't return emails when listing users
#         if kwargs['context']['view'].action == 'list':
#             del self.fields['email']
#         super().__init__(*args, **kwargs)
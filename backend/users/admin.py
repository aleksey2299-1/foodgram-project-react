from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import TokenProxy

from recipes.models import Recipe
from users.forms import UserThroughForm
from users.models import CustomBaseUser


@admin.register(CustomBaseUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff',
                    'subscribes', 'recipes')
    empty_value_display = '-пусто-'
    search_fields = ('email', 'username')
    list_filter = []
    filter_horizontal = []
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_staff',),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    @admin.display(description="Подписчики")
    def subscribes(self, user: CustomBaseUser):
        return CustomBaseUser.objects.filter(
            subscribe__email=user.email
        ).count()

    @admin.display(description="Рецепты")
    def recipes(self, user: CustomBaseUser):
        return Recipe.objects.filter(author=user).count()


@admin.register(CustomBaseUser.subscribe.through)
class ShoppingCartRecipeUserRelationAdmin(admin.ModelAdmin):
    form = UserThroughForm
    list_display = ('from_custombaseuser', 'to_custombaseuser')
    empty_value_display = '-пусто-'

    def __init__(self, *args, **kwargs):
        args[0]._meta.verbose_name = 'объекты подписки'
        args[0]._meta.verbose_name_plural = 'Пользователь подписан на'
        super().__init__(*args, **kwargs)


admin.site.unregister(Group)
admin.site.unregister(TokenProxy)

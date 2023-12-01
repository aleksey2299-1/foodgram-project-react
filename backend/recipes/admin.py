from django.contrib import admin
from django.utils.html import format_html

from recipes.forms import (FavoriteThroughForm, RecipeAdminForm,
                           ShoppingCartThroughForm)
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag, TagRecipe
from users.models import CustomBaseUser


class IngredientRecipeInline(admin.StackedInline):
    model = IngredientRecipe
    min_num = 1
    extra = 1


class TagsInline(admin.TabularInline):
    model = TagRecipe
    min_num = 1
    extra = 1


class UserInline(admin.TabularInline):
    model = CustomBaseUser
    min_num = 1
    extra = 1
    fields = ('username',)
#     # verbose_name = 'пользователь'
#     # verbose_name_plural = 'пользователи'


class RecipeInline(admin.TabularInline):
    model = Recipe
    min_num = 1
    extra = 1
    fields = ('name',)
#     # verbose_name = 'рецепт'
#     # verbose_name_plural = 'рецепты'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('measurement_unit',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('colored_tag',)

    @admin.display(description="Тэги")
    def colored_tag(self, obj):
        return format_html(
            '<span style="color: {};">{}</span>',
            obj.color,
            obj.name,
        )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    form = RecipeAdminForm
    list_display = ('author', 'name', 'in_favorites',
                    'show_tags', 'show_ingredients')
    empty_value_display = '-пусто-'
    search_fields = ('author__username', 'name')
    list_filter = ('author', 'tags')
    inlines = [TagsInline, IngredientRecipeInline]

    @admin.display(description="В избранном")
    def in_favorites(self, obj):
        return obj.added_to_favorites.count()

    @admin.display(description="Тэги")
    def show_tags(self, obj):
        tag_list = []
        for tag in obj.tags.all():
            tag_list.append(tag.name)
        return ', '.join(tag_list)

    @admin.display(description="Ингредиенты")
    def show_ingredients(self, obj):
        ingredients_list = []
        for ingredient in obj.ingredients.all():
            ingredients_list.append(ingredient.__str__())
        return ', '.join(ingredients_list)


@admin.register(Recipe.added_to_favorites.through)
class FavoriteRecipeUserRelationAdmin(admin.ModelAdmin):
    form = FavoriteThroughForm
    list_display = ('recipe', 'custombaseuser')
    empty_value_display = '-пусто-'

    def __init__(self, *args, **kwargs):
        args[0]._meta.verbose_name = 'Объекты избранного'
        args[0]._meta.verbose_name_plural = 'Рецепт в избранном у'
        super().__init__(*args, **kwargs)


@admin.register(Recipe.shopping_cart.through)
class ShoppingCartRecipeUserRelationAdmin(admin.ModelAdmin):
    form = ShoppingCartThroughForm
    list_display = ('recipe', 'custombaseuser')
    empty_value_display = '-пусто-'

    def __init__(self, *args, **kwargs):
        args[0]._meta.verbose_name = 'Объекты корзины'
        args[0]._meta.verbose_name_plural = 'Рецепт в корзине у'
        super().__init__(*args, **kwargs)


admin.site.register(IngredientRecipe)
admin.site.register(TagRecipe)

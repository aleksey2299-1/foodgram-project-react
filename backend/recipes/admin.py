from django.contrib import admin
from django.utils.html import format_html

from recipes.forms import RecipeAdminForm
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag, TagRecipe


class IngredientRecipeInline(admin.StackedInline):
    model = IngredientRecipe
    min_num = 1
    extra = 1


class TagsInline(admin.TabularInline):
    model = TagRecipe
    min_num = 1
    extra = 1


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
    search_fields = ('author', 'name')
    list_filter = ('author', 'tags')
    readonly_fields = ('author',)
    inlines = [TagsInline, IngredientRecipeInline]

    @admin.display(description="В избранном")
    def in_favorites(self, recipe: Recipe):
        return recipe.added_to_favorites.count()

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

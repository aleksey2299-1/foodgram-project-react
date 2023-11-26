from django.contrib import admin

from recipes.forms import RecipeAdminForm
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag, TagRecipe


class IngredientRecipeInline(admin.StackedInline):
    model = IngredientRecipe
    extra = 1


class TagsInline(admin.TabularInline):
    model = TagRecipe
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('measurement_unit',)


class RecipeAdmin(admin.ModelAdmin):
    form = RecipeAdminForm
    list_display = ('author', 'name', 'in_favorites')
    empty_value_display = '-пусто-'
    search_fields = ('author', 'name')
    list_filter = ('author', 'tags')
    readonly_fields = ('author',)
    inlines = (TagsInline, IngredientRecipeInline)

    @admin.display(description="В избранном")
    def in_favorites(self, recipe: Recipe):
        return recipe.added_to_favorites.count()


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)

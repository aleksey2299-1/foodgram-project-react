from django.contrib import admin

from .models import Recipe, Tag, Ingredient, TagRecipe, IngredientRecipe


class IngredientRecipeInline(admin.StackedInline):
    model = IngredientRecipe
    extra = 1


class TagsInline(admin.TabularInline):
    model = TagRecipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'cooking_time', 'author', 'text',)
    empty_value_display = '-пусто-'
    readonly_fields = ('author',)
    inlines = (TagsInline, IngredientRecipeInline)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Ingredient)

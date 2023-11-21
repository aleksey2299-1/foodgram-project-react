from django.contrib import admin

from .models import Recipe, Tag, Ingridient


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'time', 'desc')
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Ingridient)

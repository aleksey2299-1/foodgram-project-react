from django.contrib import admin

from .models import CustomBaseUser


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    empty_value_display = '-пусто-'


admin.site.register(CustomBaseUser, UserAdmin)
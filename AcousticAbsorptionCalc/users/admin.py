from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    fields = ("id", "first_name", "last_name")


admin.site.register(User, UserAdmin)

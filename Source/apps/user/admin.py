from django.contrib import admin
from apps.user.models import User


class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)
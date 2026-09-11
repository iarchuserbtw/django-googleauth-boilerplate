from django.contrib import admin

from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [f.name for f in User._meta.fields if f.name != 'password']

    
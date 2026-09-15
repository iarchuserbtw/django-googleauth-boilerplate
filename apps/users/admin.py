from django.contrib import admin

from .models import User, AccountDeletionRequest


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [f.name for f in User._meta.fields if f.name != 'password']
    list_filter = ('date_joined', 'updated_at', 'last_activity')
    


@admin.register(AccountDeletionRequest)
class DeletionRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'requested_at', 'delete_at', 'is_cancelled')
    list_filter = ('is_cancelled',)
    
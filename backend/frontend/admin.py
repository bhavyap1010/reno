from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'account_type', 'email_verified')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'account_type', 'email_verified'),
        }),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'account_type', 'is_staff', "email_verified")
    list_filter = ('account_type', 'is_staff', 'is_superuser', 'is_active', 'groups')

admin.site.register(CustomUser, UserAdmin)

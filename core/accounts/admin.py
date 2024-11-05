from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'is_superuser', 'is_active']
    list_filter =['email', 'is_superuser', 'is_active']
    searching_fields = ['email']
    ordering = ['email']
    
    fieldsets = (
        ('Authentication', {
            'fields': (
                'email', 'password'
                )
            }),
        ('Permissions', {
            'fields': (
                'is_superuser', 'is_staff', 'is_active'
                )
            }),
    )
    
    add_fieldsets = (
        ('Authentication', {
            'fields': (
                'email', 'password1', 'password2' 
                )
            }),
        ('Permissions', {
            'fields': (
                'is_superuser', 'is_staff', 'is_active'
                )
            }),
    )
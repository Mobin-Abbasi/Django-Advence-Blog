from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ["email", "is_superuser", "is_active", "is_verified"]
    list_filter = ["email", "is_superuser", "is_active", "is_verified"]
    searching_fields = ["email"]
    ordering = ["email"]

    fieldsets = (
        ("Authentication", {"fields": ("email", "password")}),
        (
            "Permissions",
            {"fields": ("is_superuser", "is_staff", "is_active", "is_verified")},
        ),
        ("Group Permissions", {"fields": ("groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            "Authentication",
            {"classes": ("wide",), "fields": ("email", "password1", "password2")},
        ),
        (
            "Permissions",
            {"fields": ("is_superuser", "is_staff", "is_active", "is_verified")},
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ["user", "first_name", "last_name", "created_date"]
    list_filter = ["user", "created_date"]
    searching_fields = ["user", "last_name", "first_name", "description"]
    ordering = ["user"]

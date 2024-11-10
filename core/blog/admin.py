from django.contrib import admin
from .models import Post, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "status",
        "created_date",
        "updated_date",
        "published_date",
    ]
    list_filter = ["author", "status", "created_date", "updated_date", "published_date"]
    searching_fields = [
        "title",
        "content",
        "author",
        "status",
        "created_date",
        "updated_date",
        "published_date",
    ]
    ordering = [
        "title",
        "author",
        "status",
        "created_date",
        "updated_date",
        "published_date",
    ]

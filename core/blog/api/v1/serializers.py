from rest_framework import serializers
from ...models import Post, Category


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model"""

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "category",
            "status",
            "created_date",
            "published_date",
        ]


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""

    class Meta:
        model = Category
        fields = ["id", "name"]

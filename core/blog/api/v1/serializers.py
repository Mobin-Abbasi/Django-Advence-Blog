from rest_framework import serializers
from ...models import Post, Category


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model"""

    snippet = serializers.ReadOnlyField(source="get_snippet")
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    get_absolute_url = serializers.SerializerMethodField(method_name="get_abs_url")

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "snippet",
            "category",
            "status",
            "relative_url",
            "get_absolute_url",
            "created_date",
            "published_date",
        ]

    def get_abs_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""

    class Meta:
        model = Category
        fields = ["id", "name"]

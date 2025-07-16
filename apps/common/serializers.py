from rest_framework import serializers
from .models import Page

class PageListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ['slug', 'title']

    def get_title(self, obj):
        return f"{obj.safe_translation_getter('title', 'uz')} / {obj.safe_translation_getter('title', 'ru')}"


class PageDetailSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ['slug', 'title', 'content', 'created_at', 'updated_at']

    def get_title(self, obj):
        return f"{obj.safe_translation_getter('title', 'uz')} / {obj.safe_translation_getter('title', 'ru')}"

    def get_content(self, obj):
        return f"{obj.safe_translation_getter('content', 'uz')} {obj.safe_translation_getter('content', 'ru')}"

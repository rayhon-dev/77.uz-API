from rest_framework import serializers
from .models import Page
from django.utils.translation import get_language


class PageListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ['slug', 'title']

    def get_title(self, obj):
        lang = get_language() or 'uz'
        return getattr(obj, f"title_{lang}", obj.title)


class PageDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ['slug', 'title', 'content', 'created_at', 'updated_at']

    def get_title(self, obj):
        lang = get_language() or 'uz'
        return getattr(obj, f"title_{lang}", obj.title)

    def get_content(self, obj):
        lang = get_language() or 'uz'
        return getattr(obj, f"content_{lang}", obj.content)
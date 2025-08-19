from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from .models import Ad, AdPhoto, Category, FavouriteProduct, MySearch, SearchCount, SearchQuery


class AdPhotoInline(admin.TabularInline):
    model = AdPhoto
    extra = 1


@admin.register(Ad)
class AdAdmin(TabbedTranslationAdmin):
    list_display = ("id", "name", "seller", "category", "is_published", "status", "view_count")
    list_filter = ("status", "is_published", "category")
    search_fields = ("name", "description")
    inlines = [AdPhotoInline]


@admin.register(Category)
class CategoryAdmin(TabbedTranslationAdmin):
    list_display = ["id", "name", "parent"]
    list_filter = ["parent"]


@admin.register(FavouriteProduct)
class FavouriteProductAdmin(admin.ModelAdmin):
    list_display = ("user", "device_id", "product", "created_at")
    search_fields = ("user__username", "device_id", "product__name")


@admin.register(MySearch)
class MySearchAdmin(admin.ModelAdmin):
    list_display = ("user", "search_query", "category", "region", "created_at")
    search_fields = ("search_query", "user__username")


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    search_fields = ("name",)


@admin.register(SearchCount)
class SearchCountAdmin(admin.ModelAdmin):
    list_display = ("product", "search_count", "updated_at")

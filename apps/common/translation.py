from modeltranslation.translator import TranslationOptions, register
from store.models import Category

from .models import District, Page, Region, Setting


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ("title", "content")


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(District)
class DistrictTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Setting)
class SettingTranslationOptions(TranslationOptions):
    fields = ("working_hours",)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name",)

from modeltranslation.translator import TranslationOptions, register
from .models import Category, Ad


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Ad)
class AdsTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

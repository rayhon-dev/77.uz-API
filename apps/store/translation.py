from modeltranslation.translator import TranslationOptions, register
from .models import Category, Ad


@register(Ad)
class AdsTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

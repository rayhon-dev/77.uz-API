from modeltranslation.translator import translator, TranslationOptions
from .models import Page, Region, District, Setting

class PageTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)

class DistrictTranslationOptions(TranslationOptions):
    fields = ('name',)

class SettingTranslationOptions(TranslationOptions):
    fields = ('working_hours',)

translator.register(Page, PageTranslationOptions)
translator.register(Region, RegionTranslationOptions)
translator.register(District, DistrictTranslationOptions)
translator.register(Setting, SettingTranslationOptions)

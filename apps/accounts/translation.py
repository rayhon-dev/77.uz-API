from modeltranslation.translator import register, TranslationOptions
from .models import CustomUser, Address
from store.models import Category


@register(CustomUser)
class CustomUserTranslationOptions(TranslationOptions):
    fields = ('full_name', 'project_name',)


@register(Address)
class AddressTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
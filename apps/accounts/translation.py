from modeltranslation.translator import register, TranslationOptions
from .models import CustomUser, Address


@register(CustomUser)
class CustomUserTranslationOptions(TranslationOptions):
    fields = ('full_name', 'project_name',)


@register(Address)
class AddressTranslationOptions(TranslationOptions):
    fields = ('name',)

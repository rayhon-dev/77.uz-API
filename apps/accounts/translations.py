from modeltranslation.translator import translator, TranslationOptions
from .models import CustomUser

class CustomUserTranslationOptions(TranslationOptions):
    fields = ('full_name', 'project_name', 'address_name',)

translator.register(CustomUser, CustomUserTranslationOptions)

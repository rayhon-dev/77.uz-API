from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from .models import CustomUser, Address
from django.utils.translation import gettext_lazy as _


@admin.register(Address)
class AddressAdmin(TabbedTranslationAdmin):
    list_display = ['id', 'name', 'lat', 'long']
    search_fields = ['name']


@admin.register(CustomUser)
class CustomUserAdmin(TabbedTranslationAdmin):
    list_display = ('phone_number', 'full_name', 'project_name', 'status', 'is_active', 'manual_password_display')
    readonly_fields = ('phone_number',)

    fieldsets = (
        (_('User Info'), {
            'fields': ('full_name', 'project_name', 'phone_number', 'category', 'address')
        }),
        (_('Status'), {
            'fields': ('status', 'is_active', 'is_seller', 'manual_password')
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.manual_password:
            obj.set_password(obj.manual_password)
            obj.manual_password = None
        super().save_model(request, obj, form, change)


    def manual_password_display(self, obj):
        return obj.manual_password or '---'
    manual_password_display.short_description = _('Password')

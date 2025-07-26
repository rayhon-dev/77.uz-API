from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from .models import CustomUser, Address
from .utils import generate_random_password
from django.utils.translation import gettext_lazy as _


@admin.register(Address)
class AddressAdmin(TabbedTranslationAdmin):
    list_display = ['id', 'name', 'lat', 'long']
    search_fields = ['name']


@admin.register(CustomUser)
class CustomUserAdmin(TabbedTranslationAdmin):
    list_display = ('phone_number', 'full_name', 'project_name', 'status', 'is_active')
    readonly_fields = ('phone_number', 'generated_password_display')
    fieldsets = (
        (_('User Info'), {
            'fields': ('full_name', 'project_name', 'phone_number', 'category', 'address')
        }),
        (_('Status'), {
            'fields': ('status', 'is_active', 'is_seller', 'generated_password_display')
        }),
    )

    def save_model(self, request, obj, form, change):
        old_obj = CustomUser.objects.filter(pk=obj.pk).first()

        if old_obj and old_obj.status != 'approved' and obj.status == 'approved':
            new_password = generate_random_password()
            obj.set_password(new_password)
            obj.is_active = True
            obj._generated_password = new_password

        super().save_model(request, obj, form, change)

    def generated_password_display(self, obj):
        return getattr(obj, '_generated_password', '----')
    generated_password_display.short_description = _('Generated Password (show only after approval)')

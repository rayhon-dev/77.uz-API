from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from .models import CustomUser


@admin.register(CustomUser)
class SellerUserAdmin(TabbedTranslationAdmin):
    list_display = ("full_name", "phone_number", "status", "is_active", "role")
    list_filter = ("status", "is_active", "role")
    search_fields = ("full_name", "phone_number")
    readonly_fields = ("last_login",)

    fieldsets = (
        (None, {"fields": ("phone_number", "full_name", "project_name", "profile_photo")}),
        (
            "Tizim huquqlari",
            {
                "fields": (
                    "role",
                    "status",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Qo‘shimcha", {"fields": ("category", "address", "last_login")}),
        ("Parol", {"fields": ("password",)}),
    )

    def save_model(self, request, obj, form, change):
        if "password" in form.changed_data:
            obj.set_password(obj.password)
        obj.save()

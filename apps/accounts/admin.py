from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, ProductCategory
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from .models import CustomUser, ProductCategory


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']



# users/admin.py
from django.contrib import admin, messages
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from .utils import generate_random_password


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'full_name', 'is_active', 'is_approved']
    actions = ['approve_and_generate_password']

    @admin.action(description="Tasdiqlash va parol yaratish")
    def approve_and_generate_password(self, request, queryset):
        for user in queryset:
            if not user.is_active:
                password = generate_random_password()
                user.password = make_password(password)
                user.is_active = True
                user.is_approved = True
                user.save()
                messages.success(request, f"{user.username} uchun parol: {password}")
            else:
                messages.warning(request, f"{user.username} allaqachon aktiv.")

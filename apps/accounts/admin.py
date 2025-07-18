from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, ProductCategory
from django.utils.translation import gettext_lazy as _

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('id', 'phone_number', 'full_name', 'is_approved', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_approved', 'is_staff', 'is_superuser')
    readonly_fields = ('last_login', 'date_joined')

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (_('Personal info'), {'fields': ('full_name', 'project_name', 'category', 'address_name', 'address_lat', 'address_long')}),
        (_('Permissions'), {'fields': ('is_active', 'is_approved', 'is_staff', 'is_superuser', 'is_seller', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'phone_number', 'username', 'email', 'password1', 'password2',
                'is_active', 'is_approved', 'is_staff', 'is_superuser', 'is_seller'
            ),
        }),
    )

    search_fields = ('phone_number', 'full_name')
    ordering = ('-id',)

    def save_model(self, request, obj, form, change):
        newly_approved = not obj.is_approved and form.cleaned_data.get('is_approved', False)
        super().save_model(request, obj, form, change)

        if newly_approved:
            # Bu joyda siz SMS yoki email yuborishingiz mumkin
            print(f"Yuborish kerak: login={obj.phone_number}")

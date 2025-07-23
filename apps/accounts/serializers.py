from rest_framework import serializers
from .models import CustomUser, ProductCategory


class AddressSerializer(serializers.Serializer):
    name = serializers.CharField()
    lat = serializers.FloatField()
    long = serializers.FloatField()


class SellerRegistrationSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    address = AddressSerializer()

    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'project_name', 'category_id', 'phone_number', 'address', 'status']

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        category_id = validated_data.pop('category_id')
        category = ProductCategory.objects.get(id=category_id)  # 'category_id' orqali 'ProductCategory'ni olish

        user = CustomUser.objects.create(
            **validated_data,
            category=category,
            is_active=False,
            is_approved=False,
            is_seller=True
        )

        # Address ma'lumotlarini foydalanuvchiga qo‘shamiz
        user.address_name = address_data['name']
        user.address_lat = address_data['lat']
        user.address_long = address_data['long']
        user.save()

        return user

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "full_name": instance.full_name,
            "project_name": instance.project_name,
            "category_id": instance.category.id if instance.category else None,
            "phone_number": instance.phone_number,
            "address": {
                "name": instance.address_name,
                "lat": instance.address_lat,
                "long": instance.address_long,
            },
            "status": "pending"  # Response'da statusni ko‘rsatamiz
        }

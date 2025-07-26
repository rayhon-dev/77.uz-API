from rest_framework import serializers
from .models import CustomUser, Address
from store.models import Category


class CategoryMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['name', 'lat', 'long']


class SellerRegistrationSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    address = AddressSerializer()

    category = CategoryMiniSerializer(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'full_name', 'project_name', 'phone_number',
            'category_id', 'category', 'address', 'status'
        ]

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        category_id = validated_data.pop('category_id')
        address = Address.objects.create(**address_data)
        category = Category.objects.get(id=category_id)

        user = CustomUser.objects.create(
            **validated_data,
            category=category,
            address=address,
            is_active=False,
            is_seller=True
        )
        return user

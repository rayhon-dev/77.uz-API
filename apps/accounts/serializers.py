from rest_framework import serializers
from .models import CustomUser, Address
from store.models import Category
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import UntypedToken

User = get_user_model()



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




class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    phone_number = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        password = attrs.get("password")

        user = authenticate(phone_number=phone_number, password=password)

        if not user or not user.is_active:
            raise AuthenticationFailed('No active account found with the given credentials', code='authorization')

        data = super().validate(attrs)
        return data



class CustomTokenVerifySerializer(TokenVerifySerializer):
    token_class = UntypedToken

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validated_data["valid"] = True
        validated_data["user_id"] = self.user.id if hasattr(self, "user") else None
        return validated_data


class UserMeSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'phone_number', 'profile_photo', 'address']

    def get_profile_photo(self, obj):
        if obj.profile_photo and hasattr(obj.profile_photo, 'url'):
            return obj.profile_photo.url
        return None

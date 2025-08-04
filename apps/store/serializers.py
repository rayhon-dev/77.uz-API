from rest_framework import serializers
from .models import Ad, AdPhoto
from store.models import Category
from accounts.models import CustomUser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'parent']


class CategoryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class SellerShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'phone_number', 'profile_photo']


class AdCreateSerializer(serializers.ModelSerializer):
    photos = serializers.ListField(child=serializers.ImageField(), write_only=True)
    photo = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    seller = SellerShortSerializer(read_only=True)

    class Meta:
        model = Ad
        fields = [
            'id', 'name_uz', 'name_ru', 'slug',
            'category', 'description_uz', 'description_ru',
            'price', 'photos', 'photo', 'published_at',
            'address', 'seller', 'is_liked', 'updated_time'
        ]
        extra_kwargs = {
            'name_uz': {'write_only': True},
            'name_ru': {'write_only': True},
            'description_uz': {'write_only': True},
            'description_ru': {'write_only': True},
            'category': {'write_only': True},
            'photos': {'write_only': True},
        }
        read_only_fields = [
            'id', 'slug', 'photo', 'published_at',
            'address', 'seller', 'is_liked', 'updated_time'
        ]

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        photos_data = validated_data.pop('photos')
        ad = Ad.objects.create(seller=user, **validated_data)
        AdPhoto.objects.bulk_create([AdPhoto(ad=ad, image=img) for img in photos_data])
        return ad

    def get_photo(self, obj):
        first_photo = obj.photos.first()
        return first_photo.image.url if first_photo else None

    def get_address(self, obj):
        return obj.seller.address.name if obj.seller.address else None


class AdPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdPhoto
        fields = ['id', 'image']


class AdDetailSerializer(serializers.ModelSerializer):
    photos = AdPhotoSerializer(many=True, read_only=True)
    address = serializers.SerializerMethodField()
    seller = SellerShortSerializer(read_only=True)
    category = CategoryShortSerializer(read_only=True)

    class Meta:
        model = Ad
        fields = [
            'id', 'name', 'slug', 'description',
            'price', 'photos', 'published_at', 'address',
            'seller', 'category', 'is_liked', 'view_count',
            'updated_time'
        ]

    def get_address(self, obj):
        return obj.seller.address.name if obj.seller.address else None

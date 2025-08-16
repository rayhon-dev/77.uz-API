from accounts.models import CustomUser
from rest_framework import serializers
from store.models import Category

from .models import Ad, AdPhoto, FavouriteProduct


class ChildCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    icon = serializers.ImageField()


class CategoryWithChildrenSerializer(serializers.ModelSerializer):
    children = ChildCategorySerializer(source="child", many=True)

    class Meta:
        model = Category
        fields = ["id", "name", "icon", "children"]


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "icon", "product_count"]

    def get_product_count(self, obj):
        return "{:,}".format(obj.product_count) if hasattr(obj, "product_count") else "0"


class CategoryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class SellerShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "full_name", "phone_number", "profile_photo"]


class AdCreateSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    photos = serializers.ListField(child=serializers.ImageField(), write_only=True)
    photo = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    seller = SellerShortSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = [
            "id",
            "name",
            "name_uz",
            "name_ru",
            "description",
            "slug",
            "category",
            "price",
            "photos",
            "photo",
            "published_at",
            "address",
            "seller",
            "is_liked",
            "updated_time",
        ]
        extra_kwargs = {
            "name_uz": {"write_only": True},
            "name_ru": {"write_only": True},
            "description_uz": {"write_only": True},
            "description_ru": {"write_only": True},
            "category": {"write_only": True},
            "photos": {"write_only": True},
        }
        read_only_fields = [
            "id",
            "name",
            "slug",
            "photo",
            "published_at",
            "address",
            "seller",
            "is_liked",
            "updated_time",
        ]

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user
        photos_data = validated_data.pop("photos")
        address = user.address
        ad = Ad.objects.create(seller=user, address=address, **validated_data)
        AdPhoto.objects.bulk_create([AdPhoto(ad=ad, image=img) for img in photos_data])
        return ad

    def get_photo(self, obj):
        first_photo = obj.photos.first()
        return first_photo.image.url if first_photo else None

    def get_address(self, obj):
        return obj.seller.address.name if obj.seller.address else None

    def get_is_liked(self, obj):
        request = self.context.get("request")
        user = request.user if request else None
        if user and user.is_authenticated:
            return obj.likes.filter(id=user.id).exists()
        return False

    def get_name(self, obj):
        lang = self.context["request"].LANGUAGE_CODE
        return getattr(obj, f"name_{lang}", obj.name_uz)


class AdPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdPhoto
        fields = ["id", "image"]


class AdDetailSerializer(serializers.ModelSerializer):
    photos = AdPhotoSerializer(many=True, read_only=True)
    address = serializers.SerializerMethodField()
    seller = SellerShortSerializer(read_only=True)
    category = CategoryShortSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "photos",
            "published_at",
            "address",
            "seller",
            "category",
            "is_liked",
            "view_count",
            "updated_time",
        ]

    def get_address(self, obj):
        return obj.seller.address.name if obj.seller.address else None

    def get_is_liked(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return obj.likes.filter(id=user.id).exists()
        return False

    def to_representation(self, instance):
        data = super().to_representation(instance)
        lang = self.context["request"].LANGUAGE_CODE
        data["name"] = getattr(instance, f"name_{lang}", instance.name_uz)
        data["description"] = getattr(instance, f"description_{lang}", instance.description_uz)
        return data


class FavouriteProductSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all())

    class Meta:
        model = FavouriteProduct
        fields = ["id", "product", "device_id", "created_at"]
        read_only_fields = ["id", "created_at"]
        extra_kwargs = {
            "device_id": {"required": False},
        }

    def validate(self, attrs):
        user = self.context["request"].user
        device_id = attrs.get("device_id")

        if not user.is_authenticated and not device_id:
            raise serializers.ValidationError("Anonymous users must provide a device_id.")

        return attrs

    def create(self, validated_data):
        user = (
            self.context["request"].user if self.context["request"].user.is_authenticated else None
        )
        device_id = validated_data.get("device_id")
        product = validated_data["product"]

        if user:
            obj, _ = FavouriteProduct.objects.get_or_create(user=user, product=product)
        else:
            obj, _ = FavouriteProduct.objects.get_or_create(device_id=device_id, product=product)

        return obj

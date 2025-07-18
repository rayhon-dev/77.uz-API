from rest_framework import serializers
from .models import CustomUser


class AddressSerializer(serializers.Serializer):
    name = serializers.CharField()
    lat = serializers.FloatField()
    long = serializers.FloatField()

class SellerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'full_name', 'project_name', 'category', 'address_name', 'address_lat', 'address_long']

    def create(self, validated_data):
        return CustomUser.objects.create(
            **validated_data,
            is_active=False,
            is_approved=False,
            is_seller=True
        )

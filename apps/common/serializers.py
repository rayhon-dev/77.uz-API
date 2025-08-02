from rest_framework import serializers


class PageListSerializer(serializers.Serializer):
    slug = serializers.SlugField()
    title = serializers.CharField()


class PageDetailSerializer(serializers.Serializer):
    slug = serializers.SlugField()
    title = serializers.CharField()
    content = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class DistrictSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class RegionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    districts = DistrictSerializer(many=True)


class SettingSerializer(serializers.Serializer):
    phone = serializers.CharField()
    support_email = serializers.EmailField()
    app_version = serializers.CharField()
    maintenance_mode = serializers.BooleanField()
    working_hours = serializers.CharField()


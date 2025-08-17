import django_filters

from .models import Ad


class AdFilter(django_filters.FilterSet):
    price__gte = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price__lte = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    region_id = django_filters.NumberFilter(field_name="seller__region_id")
    district_id = django_filters.NumberFilter(field_name="seller__district_id")

    seller_id = django_filters.NumberFilter(field_name="seller_id")

    is_top = django_filters.BooleanFilter(field_name="is_top")

    category_ids = django_filters.CharFilter(method="filter_categories")

    class Meta:
        model = Ad
        fields = [
            "price__gte",
            "price__lte",
            "seller_id",
            "region_id",
            "district_id",
            "is_top",
        ]

    def filter_categories(self, queryset, name, value):
        ids = [int(pk) for pk in value.split(",") if pk.isdigit()]
        return queryset.filter(category_id__in=ids)

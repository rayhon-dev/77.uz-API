from drf_yasg import openapi

# ----------------------------
# Ad Schemas
# ----------------------------

ad_create_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=[
        "name_uz",
        "name_ru",
        "category",
        "description_uz",
        "description_ru",
        "price",
        "photos",
    ],
    properties={
        "name_uz": openapi.Schema(
            type=openapi.TYPE_STRING, description="Title in Uzbek", example="Telefon"
        ),
        "name_ru": openapi.Schema(
            type=openapi.TYPE_STRING, description="Title in Russian", example="Телефон"
        ),
        "category": openapi.Schema(type=openapi.TYPE_INTEGER, description="Category ID", example=5),
        "description_uz": openapi.Schema(
            type=openapi.TYPE_STRING, description="Description in Uzbek", example="Yangi telefon"
        ),
        "description_ru": openapi.Schema(
            type=openapi.TYPE_STRING, description="Description in Russian", example="Новый телефон"
        ),
        "price": openapi.Schema(type=openapi.TYPE_INTEGER, description="Price", example=250),
        "photos": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_FILE),
            description="List of image files",
        ),
    },
)

ad_detail_response = openapi.Response(
    description="Ad detail response",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
            "name": openapi.Schema(type=openapi.TYPE_STRING, example="Phone"),
            "slug": openapi.Schema(type=openapi.TYPE_STRING, example="phone"),
            "description": openapi.Schema(type=openapi.TYPE_STRING, example="Brand new phone..."),
            "price": openapi.Schema(type=openapi.TYPE_INTEGER, example=250),
            "photos": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        "image": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            format="uri",
                            example="/media/products/img1.jpg",
                        ),
                    },
                ),
            ),
            "published_at": openapi.Schema(
                type=openapi.TYPE_STRING, format="date-time", example="2025-08-07T12:34:56Z"
            ),
            "address": openapi.Schema(type=openapi.TYPE_STRING, example="Tashkent"),
            "seller": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=2),
                    "full_name": openapi.Schema(type=openapi.TYPE_STRING, example="John Doe"),
                    "phone_number": openapi.Schema(
                        type=openapi.TYPE_STRING, example="+998901234567"
                    ),
                    "profile_photo": openapi.Schema(
                        type=openapi.TYPE_STRING, format="uri", example="/media/profile/photo.jpg"
                    ),
                },
            ),
            "category": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
                    "name": openapi.Schema(type=openapi.TYPE_STRING, example="Electronics"),
                },
            ),
            "is_liked": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
            "view_count": openapi.Schema(type=openapi.TYPE_INTEGER, example=13),
            "updated_time": openapi.Schema(
                type=openapi.TYPE_STRING, format="date-time", example="2025-08-07T13:00:00Z"
            ),
        },
    ),
)

ad_create_response = openapi.Response(
    description="Ad successfully created",
    schema=ad_detail_response.schema,
)


seller_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=456),
        "full_name": openapi.Schema(type=openapi.TYPE_STRING, example="Karimov Akmal"),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING, example="+998901234567"),
        "profile_photo": openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_URI,
            example="https://admin.77.uz/media/profiles/seller_photo.jpg",
        ),
    },
)

ad_list_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=12345),
        "name": openapi.Schema(type=openapi.TYPE_STRING, example="iPhone 15 Pro Max 256GB"),
        "slug": openapi.Schema(type=openapi.TYPE_STRING, example="iphone-15-pro-max-256gb"),
        "price": openapi.Schema(type=openapi.TYPE_INTEGER, example=15000000),
        "photo": openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_URI,
            example="https://admin.77.uz/media/products/iphone15_main.jpg",
        ),
        "published_at": openapi.Schema(
            type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, example="2024-01-15T10:30:00Z"
        ),
        "address": openapi.Schema(
            type=openapi.TYPE_STRING, example="Toshkent shahar, Chilonzor tumani"
        ),
        "seller": seller_schema,
        "is_liked": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
        "updated_time": openapi.Schema(
            type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, example="2024-01-15T10:30:00Z"
        ),
    },
)

ad_list_parameters = [
    openapi.Parameter(
        "search",
        openapi.IN_QUERY,
        description="Qidiruv so'zi",
        type=openapi.TYPE_STRING,
        example="iPhone",
    ),
    openapi.Parameter(
        "price__gte",
        openapi.IN_QUERY,
        description="Minimal narx",
        type=openapi.TYPE_INTEGER,
        example=1000000,
    ),
    openapi.Parameter(
        "price__lte",
        openapi.IN_QUERY,
        description="Maksimal narx",
        type=openapi.TYPE_INTEGER,
        example=20000000,
    ),
    openapi.Parameter(
        "is_top",
        openapi.IN_QUERY,
        description="Top e'lonlar filtri",
        type=openapi.TYPE_STRING,
        example="true",
    ),
    openapi.Parameter(
        "seller_id",
        openapi.IN_QUERY,
        description="Sotuvchi ID filtri",
        type=openapi.TYPE_INTEGER,
        example=456,
    ),
    openapi.Parameter(
        "district_id",
        openapi.IN_QUERY,
        description="Tuman ID filtri",
        type=openapi.TYPE_INTEGER,
        example=101,
    ),
    openapi.Parameter(
        "region_id",
        openapi.IN_QUERY,
        description="Viloyat ID filtri",
        type=openapi.TYPE_INTEGER,
        example=1,
    ),
    openapi.Parameter(
        "category_ids",
        openapi.IN_QUERY,
        description="Kategoriya IDlari filtri",
        type=openapi.TYPE_STRING,
        example="15,16,17",
    ),
    openapi.Parameter(
        "ordering",
        openapi.IN_QUERY,
        description="Saralash tartibi",
        type=openapi.TYPE_STRING,
        example="-published_at",
    ),
    openapi.Parameter(
        "page", openapi.IN_QUERY, description="Sahifa raqami", type=openapi.TYPE_INTEGER, example=1
    ),
    openapi.Parameter(
        "page_size",
        openapi.IN_QUERY,
        description="Sahifa hajmi",
        type=openapi.TYPE_INTEGER,
        example=20,
    ),
]

# ----------------------------
# Category Schemas
# ----------------------------

category_list_response = openapi.Response(
    description="Category list with product count",
    schema=openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                "name": openapi.Schema(type=openapi.TYPE_STRING, example="Electronics"),
                "icon": openapi.Schema(
                    type=openapi.TYPE_STRING, format="uri", example="/media/categories/icon.png"
                ),
                "product_count": openapi.Schema(type=openapi.TYPE_STRING, example="12"),
            },
        ),
    ),
)

child_category_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=15),
        "name": openapi.Schema(type=openapi.TYPE_STRING, example="Telefonlar / Телефоны"),
        "icon": openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_URI,
            example="https://admin.77.uz/media/icons/phone.svg",
        ),
    },
    required=["id", "name", "icon"],
)

categories_with_children_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
        "name": openapi.Schema(type=openapi.TYPE_STRING, example="Elektronika / Электроника"),
        "icon": openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_URI,
            example="https://admin.77.uz/media/icons/electronics.svg",
        ),
        "children": openapi.Schema(type=openapi.TYPE_ARRAY, items=child_category_schema),
    },
)


sub_category_list_response = openapi.Response(
    description="Subcategories list",
    schema=openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=2),
                "name": openapi.Schema(type=openapi.TYPE_STRING, example="Phones"),
                "icon": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="uri",
                    example="/media/categories/phone-icon.png",
                ),
                "product_count": openapi.Schema(type=openapi.TYPE_STRING, example="7"),
            },
        ),
    ),
)

# ----------------------------
# Favourite Product Schemas
# ----------------------------

favourite_product_seller_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["product"],
    properties={
        "product": openapi.Schema(type=openapi.TYPE_INTEGER, description="Product ID", example=1)
    },
)

favourite_product_guest_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["product", "device_id"],
    properties={
        "product": openapi.Schema(type=openapi.TYPE_INTEGER, description="Product ID", example=1),
        "device_id": openapi.Schema(
            type=openapi.TYPE_STRING, description="Device ID", example="abc123"
        ),
    },
)

favourite_product_response_for_seller = openapi.Response(
    description="Favourite product response",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
            "product": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
            "created_at": openapi.Schema(
                type=openapi.TYPE_STRING, format="date-time", example="2025-08-07T12:34:56Z"
            ),
        },
    ),
)

favourite_product_response = openapi.Response(
    description="Favourite product response",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
            "product": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
            "device_id": openapi.Schema(type=openapi.TYPE_STRING, example="abc123"),
            "created_at": openapi.Schema(
                type=openapi.TYPE_STRING, format="date-time", example="2025-08-07T12:34:56Z"
            ),
        },
    ),
)


my_favourite_products_response = openapi.Response(
    description="List of favourite products",
    schema=openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                "name": openapi.Schema(type=openapi.TYPE_STRING, example="Phone"),
                "slug": openapi.Schema(type=openapi.TYPE_STRING, example="phone"),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING, example="Brand new phone..."
                ),
                "price": openapi.Schema(type=openapi.TYPE_INTEGER, example=250),
                "published_at": openapi.Schema(
                    type=openapi.TYPE_STRING, format="date-time", example="2025-08-07T12:34:56Z"
                ),
                "address": openapi.Schema(type=openapi.TYPE_STRING, example="Tashkent"),
                "seller": openapi.Schema(type=openapi.TYPE_STRING, example="John Doe"),
                "photo": openapi.Schema(
                    type=openapi.TYPE_STRING, format="uri", example="/media/products/img1.jpg"
                ),
                "is_liked": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                "updated_time": openapi.Schema(
                    type=openapi.TYPE_STRING, format="date-time", example="2025-08-07T13:00:00Z"
                ),
            },
        ),
    ),
)


# ----------------------------
# MySearch Schemas
# ----------------------------

my_search_create_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["category", "search_query"],
    properties={
        "category": openapi.Schema(type=openapi.TYPE_INTEGER, description="Category ID", example=5),
        "search_query": openapi.Schema(
            type=openapi.TYPE_STRING, description="Search query", example="iPhone"
        ),
        "price_min": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="Minimum price", example=100
        ),
        "price_max": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="Maximum price", example=500
        ),
        "region_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Region ID", example=1),
    },
)

my_search_list_response = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
            "category": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
                    "name": openapi.Schema(type=openapi.TYPE_STRING, example="Electronics"),
                    "icon": openapi.Schema(type=openapi.TYPE_STRING, format="uri"),
                },
            ),
            "search_query": openapi.Schema(type=openapi.TYPE_STRING, example="iPhone"),
            "price_min": openapi.Schema(type=openapi.TYPE_INTEGER, example=100),
            "price_max": openapi.Schema(type=openapi.TYPE_INTEGER, example=500),
            "region_id": openapi.Schema(type=openapi.TYPE_STRING, example="Tashkent"),
            "created_at": openapi.Schema(
                type=openapi.TYPE_STRING, format="date-time", example="2025-08-07T12:34:56Z"
            ),
        },
    ),
)

# ----------------------------
# Search Schemas
# ----------------------------

search_category_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
        "name": openapi.Schema(type=openapi.TYPE_STRING, example="Electronics"),
        "type": openapi.Schema(type=openapi.TYPE_STRING, example="category"),
        "icon": openapi.Schema(
            type=openapi.TYPE_STRING, format="uri", example="/media/categories/icon.png"
        ),
    },
)

search_product_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
        "name": openapi.Schema(type=openapi.TYPE_STRING, example="iPhone 14"),
        "type": openapi.Schema(type=openapi.TYPE_STRING, example="product"),
        "icon": openapi.Schema(
            type=openapi.TYPE_STRING, format="uri", example="/media/products/img1.jpg"
        ),
    },
)

search_complete_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Product ID"),
        "name": openapi.Schema(type=openapi.TYPE_STRING, description="Product name"),
        "icon": openapi.Schema(
            type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description="Product icon URL"
        ),
    },
)

search_count_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
        "category": openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
        "search_count": openapi.Schema(type=openapi.TYPE_INTEGER, example=10),
        "updated_at": openapi.Schema(
            type=openapi.TYPE_STRING, format="date-time", example="2025-08-07T12:34:56Z"
        ),
    },
)

popular_search_response = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
            "name": openapi.Schema(type=openapi.TYPE_STRING, example="iPhone 14"),
            "icon": openapi.Schema(
                type=openapi.TYPE_STRING, format="uri", example="/media/products/img1.jpg"
            ),
            "search_count": openapi.Schema(type=openapi.TYPE_INTEGER, example=20),
        },
    ),
)


my_search_create_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="ID of the search entry", example=1
        ),
        "category": openapi.Schema(type=openapi.TYPE_INTEGER, description="Category ID", example=5),
        "search_query": openapi.Schema(
            type=openapi.TYPE_STRING, description="Search query", example="iPhone"
        ),
        "price_min": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="Minimum price", example=100, nullable=True
        ),
        "price_max": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="Maximum price", example=500, nullable=True
        ),
        "region_id": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="Region ID", example=1, nullable=True
        ),
        "created_at": openapi.Schema(
            type=openapi.FORMAT_DATETIME,
            description="Creation timestamp",
            example="2025-08-20T12:34:56Z",
        ),
    },
)

# ----------------- AdPhoto -----------------
ad_photo_create_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["product_id", "image"],
    properties={
        "product_id": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="ID of the Ad", example=10
        ),
        "image": openapi.Schema(
            type=openapi.TYPE_STRING, format="binary", description="Image file"
        ),
        "is_main": openapi.Schema(
            type=openapi.TYPE_BOOLEAN, description="Whether this photo is main", default=False
        ),
    },
)

ad_photo_create_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the photo", example=1),
        "image": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Image URL",
            example="https://example.com/photo.jpg",
        ),
        "is_main": openapi.Schema(
            type=openapi.TYPE_BOOLEAN, description="Is main photo", example=True
        ),
        "product_id": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="ID of the related Ad", example=10
        ),
        "created_at": openapi.Schema(
            type=openapi.FORMAT_DATETIME,
            description="Creation timestamp",
            example="2025-08-20T12:34:56Z",
        ),
    },
)

my_ad_update_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the Ad", example=12345),
        "name": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Name of the product",
            example="iPhone 15 Pro Max 256GB Titanium",
        ),
        "slug": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Slug generated from the product name",
            example="iphone-15-pro-max-256gb-titanium",
        ),
        "description": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Description of the product",
            example="Yangi iPhone 15 Pro Max, 256GB xotira, titanium rang. Kafolat bilan.",
        ),
        "category": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="ID of the category", example=15
        ),
        "price": openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description="Price of the product in local currency",
            example=15000000,
        ),
        "photos": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description="Photo URL"
            ),
            description="List of product photos",
        ),
        "published_at": openapi.Schema(
            type=openapi.FORMAT_DATETIME,
            description="Published timestamp",
            example="2024-01-15T10:30:00Z",
        ),
        "status": openapi.Schema(
            type=openapi.TYPE_STRING, description="Status of the product", example="active"
        ),
        "view_count": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="Number of views", example=125
        ),
        "updated_time": openapi.Schema(
            type=openapi.FORMAT_DATETIME,
            description="Last updated timestamp",
            example="2024-01-15T10:30:00Z",
        ),
    },
)

my_ad_update_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Name of the product",
            example="iPhone 15 Pro Max 256GB Titanium",
        ),
        "description": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Description of the product",
            example="Yangi iPhone 15 Pro Max, 256GB xotira, titanium rang. Kafolat bilan.",
        ),
        "category": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="ID of the category", example=15
        ),
        "price": openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description="Price of the product in local currency",
            example=15000000,
        ),
        "photos": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description="Photo URL"
            ),
            description="List of product photos",
        ),
        "status": openapi.Schema(
            type=openapi.TYPE_STRING, description="Status of the product", example="active"
        ),
    },
)

my_ad_detail_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=12345),
        "name": openapi.Schema(
            type=openapi.TYPE_STRING, example="iPhone 15 Pro Max 256GB Titanium"
        ),
        "slug": openapi.Schema(
            type=openapi.TYPE_STRING, example="iphone-15-pro-max-256gb-titanium"
        ),
        "description": openapi.Schema(
            type=openapi.TYPE_STRING,
            example="Yangi iPhone 15 Pro Max, 256GB xotira, titanium rang. Kafolat bilan.",
        ),
        "category": openapi.Schema(type=openapi.TYPE_INTEGER, example=15),
        "price": openapi.Schema(type=openapi.TYPE_INTEGER, example=15000000),
        "photos": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
            example=[
                "https://admin.77.uz/media/products/iphone15_main.jpg",
                "https://admin.77.uz/media/products/iphone15_2.jpg",
            ],
        ),
        "published_at": openapi.Schema(
            type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, example="2024-01-15T10:30:00Z"
        ),
        "status": openapi.Schema(type=openapi.TYPE_STRING, example="active"),
        "view_count": openapi.Schema(type=openapi.TYPE_INTEGER, example=125),
        "updated_time": openapi.Schema(
            type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, example="2024-01-15T10:30:00Z"
        ),
    },
)

my_ads_list_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=12345),
        "name": openapi.Schema(type=openapi.TYPE_STRING, example="iPhone 15 Pro Max 256GB"),
        "slug": openapi.Schema(type=openapi.TYPE_STRING, example="iphone-15-pro-max-256gb"),
        "price": openapi.Schema(type=openapi.TYPE_INTEGER, example=15000000),
        "photo": openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_URI,
            example="https://admin.77.uz/media/products/iphone15_main.jpg",
        ),
        "published_at": openapi.Schema(
            type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, example="2024-01-15T10:30:00Z"
        ),
        "address": openapi.Schema(
            type=openapi.TYPE_STRING, example="Toshkent shahar, Chilonzor tumani"
        ),
        "status": openapi.Schema(type=openapi.TYPE_STRING, example="active"),
        "view_count": openapi.Schema(type=openapi.TYPE_INTEGER, example=125),
        "is_liked": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
        "updated_time": openapi.Schema(
            type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, example="2024-01-15T10:30:00Z"
        ),
    },
)

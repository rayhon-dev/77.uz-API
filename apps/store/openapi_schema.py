from drf_yasg import openapi

# ----------------------------
# Schema for Ad creation
# ----------------------------

ad_create_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=[
        "name_uz",
        "name_ru",
        "description_uz",
        "description_ru",
        "price",
        "category",
        "photos",
    ],
    properties={
        "name_uz": openapi.Schema(
            type=openapi.TYPE_STRING, description="Title of the ad in Uzbek", example="Telefon"
        ),
        "name_ru": openapi.Schema(
            type=openapi.TYPE_STRING, description="Title of the ad in Russian", example="Телефон"
        ),
        "description_uz": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Description in Uzbek",
            example="Yangi telefon, kafolat bilan",
        ),
        "description_ru": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Description in Russian",
            example="Новый телефон с гарантией",
        ),
        "price": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="Price of the item", example=250
        ),
        "category": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="ID of the selected category", example=5
        ),
        "photos": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_FILE),
            description="List of image files to upload",
        ),
    },
)

# ----------------------------
# Schema for Ad detail response
# ----------------------------

ad_detail_response = openapi.Response(
    description="Details of an Ad",
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
    examples={
        "application/json": {
            "id": 1,
            "name": "Phone",
            "slug": "phone",
            "description": "Brand new phone...",
            "price": 250,
            "photos": [{"id": 1, "image": "/media/products/img1.jpg"}],
            "published_at": "2025-08-07T12:34:56Z",
            "address": "Tashkent",
            "seller": {
                "id": 2,
                "full_name": "John Doe",
                "phone_number": "+998901234567",
                "profile_photo": "/media/profile/photo.jpg",
            },
            "category": {"id": 5, "name": "Electronics"},
            "is_liked": False,
            "view_count": 13,
            "updated_time": "2025-08-07T13:00:00Z",
        }
    },
)

# ----------------------------
# Ad create response
# ----------------------------

ad_create_response = openapi.Response(
    description="Ad successfully created",
    schema=ad_detail_response.schema,
    examples=ad_detail_response.examples,
)

# ----------------------------
# Categories with children
# ----------------------------

categories_with_children_response = openapi.Response(
    description="List of parent categories with nested child categories",
    schema=openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID of the parent category", example=1
                ),
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Name of the parent category",
                    example="Electronics",
                ),
                "icon": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="uri",
                    description="Icon URL of the parent category",
                    example="/media/categories/icon.png",
                ),
                "children": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="List of child categories",
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description="ID of the child category",
                                example=2,
                            ),
                            "name": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Name of the child category",
                                example="Phones",
                            ),
                            "icon": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                format="uri",
                                description="Icon URL of the child category",
                                example="/media/categories/phone-icon.png",
                            ),
                        },
                    ),
                ),
            },
        ),
    ),
    examples={
        "application/json": [
            {
                "id": 1,
                "name": "Electronics",
                "icon": "/media/categories/icon.png",
                "children": [
                    {"id": 2, "name": "Phones", "icon": "/media/categories/phone-icon.png"},
                    {"id": 3, "name": "Laptops", "icon": "/media/categories/laptop-icon.png"},
                ],
            }
        ]
    },
)

# ----------------------------
# Flat category list with counts
# ----------------------------

category_list_response = openapi.Response(
    description="List of all categories with product counts",
    schema=openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID of the category", example=1
                ),
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Name of the category",
                    example="Furniture",
                ),
                "icon": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="uri",
                    description="Icon URL of the category",
                    example="/media/categories/chair.png",
                ),
                "product_count": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Number of ads in this category",
                    example=12,
                ),
            },
        ),
    ),
    examples={
        "application/json": [
            {
                "id": 1,
                "name": "Furniture",
                "icon": "/media/categories/chair.png",
                "product_count": 12,
            },
            {
                "id": 2,
                "name": "Books",
                "icon": "/media/categories/book.png",
                "product_count": 5,
            },
        ]
    },
)


favourite_product_create_by_id_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["device_id", "product"],
    properties={
        "device_id": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Unique device identifier for guest user",
            example="device_12345_android",
        ),
        "product": openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description="ID of the product to add to favourites",
            example=12345,
        ),
    },
)

favourite_product_response = openapi.Response(
    description="Favourite product entry details",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=789),
            "product": openapi.Schema(type=openapi.TYPE_INTEGER, example=12345),
            "device_id": openapi.Schema(type=openapi.TYPE_STRING, example="device_12345_android"),
            "created_at": openapi.Schema(
                type=openapi.TYPE_STRING, format="date-time", example="2024-01-15T10:30:00Z"
            ),
        },
    ),
    examples={
        "application/json": {
            "id": 789,
            "product": 12345,
            "device_id": "device_12345_android",
            "created_at": "2024-01-15T10:30:00Z",
        }
    },
)


favourite_product_create_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["product"],
    properties={
        "product": openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description="ID of the product to add to favourites",
            example=12345,
        ),
    },
)

favourite_product_auth_response = openapi.Response(
    description="Favourite product entry details for authenticated user",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=789),
            "product": openapi.Schema(type=openapi.TYPE_INTEGER, example=12345),
            "created_at": openapi.Schema(
                type=openapi.TYPE_STRING, format="date-time", example="2024-01-15T10:30:00Z"
            ),
        },
    ),
    examples={
        "application/json": {"id": 789, "product": 12345, "created_at": "2024-01-15T10:30:00Z"}
    },
)


favourite_product_delete_response = openapi.Response(
    description="Favourite product deleted successfully",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Favourite product deleted.")
        },
    ),
)

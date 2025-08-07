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
        "name_uz": openapi.Schema(type=openapi.TYPE_STRING, description="Title of the ad in Uzbek"),
        "name_ru": openapi.Schema(
            type=openapi.TYPE_STRING, description="Title of the ad in Russian"
        ),
        "description_uz": openapi.Schema(
            type=openapi.TYPE_STRING, description="Description in Uzbek"
        ),
        "description_ru": openapi.Schema(
            type=openapi.TYPE_STRING, description="Description in Russian"
        ),
        "price": openapi.Schema(type=openapi.TYPE_INTEGER, description="Price of the item"),
        "category": openapi.Schema(
            type=openapi.TYPE_INTEGER, description="ID of the selected category"
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
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "name": openapi.Schema(type=openapi.TYPE_STRING),
            "slug": openapi.Schema(type=openapi.TYPE_STRING),
            "description": openapi.Schema(type=openapi.TYPE_STRING),
            "price": openapi.Schema(type=openapi.TYPE_INTEGER),
            "photos": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "image": openapi.Schema(type=openapi.TYPE_STRING, format="uri"),
                    },
                ),
            ),
            "published_at": openapi.Schema(type=openapi.TYPE_STRING, format="date-time"),
            "address": openapi.Schema(type=openapi.TYPE_STRING),
            "seller": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "full_name": openapi.Schema(type=openapi.TYPE_STRING),
                    "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
                    "profile_photo": openapi.Schema(type=openapi.TYPE_STRING, format="uri"),
                },
            ),
            "category": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
            "is_liked": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            "view_count": openapi.Schema(type=openapi.TYPE_INTEGER),
            "updated_time": openapi.Schema(type=openapi.TYPE_STRING, format="date-time"),
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

ad_create_response = openapi.Response(
    description="Ad successfully created",
    schema=ad_detail_response.schema,
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


categories_with_children_response = openapi.Response(
    description="List of parent categories with nested child categories",
    schema=openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="ID of the parent category"
                ),
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Name of the parent category"
                ),
                "icon": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format="uri",
                    description="Icon URL of the parent category",
                ),
                "children": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(
                                type=openapi.TYPE_INTEGER, description="ID of the child category"
                            ),
                            "name": openapi.Schema(
                                type=openapi.TYPE_STRING, description="Name of the child category"
                            ),
                            "icon": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                format="uri",
                                description="Icon URL of the child category",
                            ),
                        },
                    ),
                    description="List of child categories",
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
                "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the category"),
                "name": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Name of the category"
                ),
                "icon": openapi.Schema(
                    type=openapi.TYPE_STRING, format="uri", description="Icon URL of the category"
                ),
                "product_count": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="Number of ads in this category"
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
            {"id": 2, "name": "Books", "icon": "/media/categories/book.png", "product_count": 5},
        ]
    },
)

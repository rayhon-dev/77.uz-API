from drf_yasg import openapi

# ------------------ Seller Registration ------------------
seller_registration_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["full_name", "project_name", "phone_number", "category", "address"],
    properties={
        "full_name": openapi.Schema(type=openapi.TYPE_STRING),
        "project_name": openapi.Schema(type=openapi.TYPE_STRING),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
        "category": openapi.Schema(type=openapi.TYPE_INTEGER),
        "address": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING),
                "lat": openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                "long": openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
            },
        ),
    },
)

seller_registration_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "full_name": openapi.Schema(type=openapi.TYPE_STRING),
        "project_name": openapi.Schema(type=openapi.TYPE_STRING),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
        "category_id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "address": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["name", "lat", "long"],
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING),
                "lat": openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                "long": openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
            },
        ),
        "status": openapi.Schema(type=openapi.TYPE_STRING),
    },
)

# ------------------ Login ------------------
login_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["phone_number", "password"],
    properties={
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
        "password": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
    },
)

login_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "access_token": openapi.Schema(type=openapi.TYPE_STRING),
        "refresh_token": openapi.Schema(type=openapi.TYPE_STRING),
        "user": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "full_name": openapi.Schema(type=openapi.TYPE_STRING),
                "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    },
)

# ------------------ Token Refresh ------------------
token_refresh_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["refresh"],
    properties={"refresh": openapi.Schema(type=openapi.TYPE_STRING)},
)

token_refresh_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={"access": openapi.Schema(type=openapi.TYPE_STRING)},
)

# ------------------ Token Verify ------------------
token_verify_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["token"],
    properties={"token": openapi.Schema(type=openapi.TYPE_STRING)},
)

token_verify_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "valid": openapi.Schema(type=openapi.TYPE_BOOLEAN),
        "user_id": openapi.Schema(type=openapi.TYPE_INTEGER),
    },
)

# ------------------ Me ------------------
me_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "full_name": openapi.Schema(type=openapi.TYPE_STRING),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
        "profile_photo": openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
        "address": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING),
                "lat": openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                "long": openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
            },
            nullable=True,
        ),
    },
)

# ------------------ Edit User ------------------
edit_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "full_name": openapi.Schema(type=openapi.TYPE_STRING),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
        "address": openapi.Schema(type=openapi.TYPE_INTEGER),
    },
)

# ------------------ Edit User ------------------
edit_partial_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "full_name": openapi.Schema(type=openapi.TYPE_STRING),
    },
)

edit_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "full_name": openapi.Schema(type=openapi.TYPE_STRING),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
        "profile_photo": openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
        "address": openapi.Schema(type=openapi.TYPE_INTEGER, nullable=True),
    },
)

# accounts/openapi_schema.py
from drf_yasg import openapi

# ===============================
# Seller Registration
# ===============================
seller_registration_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "first_name": openapi.Schema(type=openapi.TYPE_STRING, example="John"),
        "last_name": openapi.Schema(type=openapi.TYPE_STRING, example="Doe"),
        "phone": openapi.Schema(type=openapi.TYPE_STRING, example="+998901234567"),
        "email": openapi.Schema(type=openapi.TYPE_STRING, example="johndoe@example.com"),
        "store_name": openapi.Schema(type=openapi.TYPE_STRING, example="Doe Electronics"),
        "address": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, example="Yunusabad 9"),
                "lat": openapi.Schema(type=openapi.TYPE_NUMBER, format="float", example=41.311081),
                "long": openapi.Schema(type=openapi.TYPE_NUMBER, format="float", example=69.240562),
            },
        ),
    },
    required=["first_name", "last_name", "phone", "store_name", "address"],
)

seller_registration_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
        "first_name": openapi.Schema(type=openapi.TYPE_STRING, example="John"),
        "last_name": openapi.Schema(type=openapi.TYPE_STRING, example="Doe"),
        "phone": openapi.Schema(type=openapi.TYPE_STRING, example="+998901234567"),
        "email": openapi.Schema(type=openapi.TYPE_STRING, example="johndoe@example.com"),
        "store_name": openapi.Schema(type=openapi.TYPE_STRING, example="Doe Electronics"),
        "status": openapi.Schema(type=openapi.TYPE_STRING, example="pending"),
    },
)

# ===============================
# Login
# ===============================
login_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "username": openapi.Schema(type=openapi.TYPE_STRING, example="johndoe"),
        "password": openapi.Schema(type=openapi.TYPE_STRING, example="your_password123"),
    },
    required=["username", "password"],
)

login_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "access": openapi.Schema(type=openapi.TYPE_STRING, example="eyJhbGciOiJIUzI1..."),
        "refresh": openapi.Schema(type=openapi.TYPE_STRING, example="eyJhbGciOiJIUzI1..."),
        "user": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                "username": openapi.Schema(type=openapi.TYPE_STRING, example="johndoe"),
                "email": openapi.Schema(type=openapi.TYPE_STRING, example="johndoe@example.com"),
                "first_name": openapi.Schema(type=openapi.TYPE_STRING, example="John"),
                "last_name": openapi.Schema(type=openapi.TYPE_STRING, example="Doe"),
            },
        ),
    },
)

# ===============================
# Token Refresh
# ===============================
token_refresh_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "refresh": openapi.Schema(type=openapi.TYPE_STRING, example="eyJhbGciOiJIUzI1..."),
    },
    required=["refresh"],
)

token_refresh_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "access": openapi.Schema(type=openapi.TYPE_STRING, example="eyJhbGciOiJIUzI1..."),
    },
)

# ===============================
# Token Verify
# ===============================
token_verify_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "token": openapi.Schema(type=openapi.TYPE_STRING, example="eyJhbGciOiJIUzI1..."),
    },
    required=["token"],
)

token_verify_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "valid": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
    },
)

# ===============================
# Me (Profile)
# ===============================
me_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
        "username": openapi.Schema(type=openapi.TYPE_STRING, example="johndoe"),
        "email": openapi.Schema(type=openapi.TYPE_STRING, example="johndoe@example.com"),
        "first_name": openapi.Schema(type=openapi.TYPE_STRING, example="John"),
        "last_name": openapi.Schema(type=openapi.TYPE_STRING, example="Doe"),
        "phone": openapi.Schema(type=openapi.TYPE_STRING, example="+998901234567"),
    },
)

# ===============================
# Edit User (PATCH)
# ===============================
edit_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "first_name": openapi.Schema(type=openapi.TYPE_STRING, example="John"),
        "last_name": openapi.Schema(type=openapi.TYPE_STRING, example="Doe"),
        "email": openapi.Schema(type=openapi.TYPE_STRING, example="newemail@example.com"),
        "phone": openapi.Schema(type=openapi.TYPE_STRING, example="+998901234567"),
    },
    required=[],
)

edit_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
        "first_name": openapi.Schema(type=openapi.TYPE_STRING, example="John"),
        "last_name": openapi.Schema(type=openapi.TYPE_STRING, example="Doe"),
        "email": openapi.Schema(type=openapi.TYPE_STRING, example="john@example.com"),
        "username": openapi.Schema(type=openapi.TYPE_STRING, example="johndoe"),
    },
)

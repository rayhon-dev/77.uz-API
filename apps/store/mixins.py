class LikedMixin:
    def get_is_liked(self, obj):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        device_id = None

        if request and (not user or not user.is_authenticated):
            device_id = request.query_params.get("device_id") or self.context.get("device_id")

        favourites_qs = getattr(obj, "favourites", getattr(obj, "likes", None))
        if not favourites_qs:
            return False

        favourites_qs = favourites_qs.all()

        if user and user.is_authenticated:
            return favourites_qs.filter(user=user).exists()
        elif device_id:
            return favourites_qs.filter(device_id=device_id).exists()
        return False


class PhotoMixin:
    def get_photo(self, obj, main_only=False):
        if main_only:
            photo = obj.photos.filter(is_main=True).first()
        else:
            photo = obj.photos.first()
        return photo.image.url if photo else None


class LocalizedNameDescriptionMixin:
    def get_localized_field(self, obj, field):
        lang = self.context["request"].LANGUAGE_CODE
        return getattr(obj, f"{field}_{lang}", getattr(obj, f"{field}_uz"))


class IconMixin:
    def get_icon(self, obj):
        if hasattr(obj, "photos"):
            main_photo = obj.photos.filter(is_main=True).first() or obj.photos.first()
            if main_photo and main_photo.image:
                return main_photo.image.url

        if hasattr(obj, "icon") and obj.icon:
            return obj.icon.url

        return None

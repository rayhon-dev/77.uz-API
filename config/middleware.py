# common/middleware/language_middleware.py

import json
import logging

from django.conf import settings
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class APILanguageMiddleware(MiddlewareMixin):
    """
    API so'rovlari uchun til boshqaruvchi middleware
    """

    def process_request(self, request):
        # 1. Accept-Language header'dan tilni olish
        language = request.META.get("HTTP_ACCEPT_LANGUAGE")

        # 2. Query parameter'dan tilni olish (?lang=uz)
        if not language:
            language = request.GET.get("lang")

        # 3. POST data'dan tilni olish
        if not language and request.method == "POST":
            language = request.POST.get("lang")

        # 4. JSON body'dan tilni olish (agar content-type application/json bo'lsa)
        if not language and request.content_type == "application/json":
            if hasattr(request, "body"):
                try:
                    data = json.loads(request.body.decode("utf-8"))
                    language = data.get("lang")
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    logger.warning(f"JSON parse error in language middleware: {e}")

        # 5. Default tilni qo'llash
        if not language:
            language = settings.LANGUAGE_CODE

        # Faqat qo'llab-quvvatlanadigan tillarni qabul qilish
        supported_languages = [lang[0] for lang in settings.LANGUAGES]
        if language not in supported_languages:
            language = settings.LANGUAGE_CODE

        # Tilni faollashtirish
        translation.activate(language)
        request.LANGUAGE_CODE = language

    def process_response(self, request, response):
        # Response'ga til headerini qo'shish
        if hasattr(request, "LANGUAGE_CODE"):
            response["Content-Language"] = request.LANGUAGE_CODE
        return response

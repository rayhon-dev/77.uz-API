import json
import logging

from django.conf import settings
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class APILanguageMiddleware(MiddlewareMixin):

    def process_request(self, request):
        language = request.META.get("HTTP_ACCEPT_LANGUAGE")

        if not language:
            language = request.GET.get("lang")

        if not language and request.method == "POST":
            language = request.POST.get("lang")

        if not language and request.content_type == "application/json":
            if hasattr(request, "body"):
                try:
                    data = json.loads(request.body.decode("utf-8"))
                    language = data.get("lang")
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    logger.warning(f"JSON parse error in language middleware: {e}")

        if not language:
            language = settings.LANGUAGE_CODE

        supported_languages = [lang[0] for lang in settings.LANGUAGES]
        if language not in supported_languages:
            language = settings.LANGUAGE_CODE

        translation.activate(language)
        request.LANGUAGE_CODE = language

    def process_response(self, request, response):
        if hasattr(request, "LANGUAGE_CODE"):
            response["Content-Language"] = request.LANGUAGE_CODE
        return response

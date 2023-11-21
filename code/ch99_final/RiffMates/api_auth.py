# RiffMates/api_auth.py
from django.conf import settings
from ninja.security import APIKeyHeader


class APIKey(APIKeyHeader):
    param_name = "X-API-KEY"

    def authenticate(self, request, key):
        if key == settings.NINJA_API_KEY:
            return key


api_key = APIKey()

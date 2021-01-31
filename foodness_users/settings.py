from django.conf import settings

CUSTOM_SETTINGS = getattr(settings, "FOODNESS_USERS", {})

app_settings = {
    "ALLOWED_AVATAR_EXTENSIONS": ["jpg", "jpeg", "png"],
}

app_settings.update(CUSTOM_SETTINGS)

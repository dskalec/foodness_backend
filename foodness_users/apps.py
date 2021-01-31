from django.apps import AppConfig
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _


current_app_label = "foodness_users"


class FoodnessUsersConfig(AppConfig):
    label = current_app_label
    name = "foodness_users"
    verbose_name = _("Foodness users")

    def ready(self):
        from .signals import create_user_profile
        from django.contrib.auth import get_user_model

        User = get_user_model()

        post_save.connect(create_user_profile, User)

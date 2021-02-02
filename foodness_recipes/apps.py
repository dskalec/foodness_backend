from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


current_app_label = "foodness_recipes"


class FoodnessRecipesConfig(AppConfig):
    label = current_app_label
    name = "foodness_recipes"
    verbose_name = _("Foodness recipes")

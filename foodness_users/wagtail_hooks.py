from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import UserProfile


class UserProfileAdmin(ModelAdmin):
    model = UserProfile
    menu_icon = "user"
    menu_order = 300
    add_to_settings_menu = False
    list_display = ["user", "birth_date", "gender"]
    search_fields = [
        "user__username",
        "user__email",
    ]


modeladmin_register(UserProfileAdmin)

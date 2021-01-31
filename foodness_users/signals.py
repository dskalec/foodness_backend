from django.apps import apps


def create_user_profile(sender, instance, created, *args, **kwargs):
    UserProfile = apps.get_model("foodness_users", "UserProfile")

    if created:
        UserProfile.create_for_user(instance)

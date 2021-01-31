import os
import uuid

from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel

from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.utils import IntegrityError
from django.utils.translation import gettext_lazy as _

from .apps import current_app_label
from .settings import app_settings

User = get_user_model()


def upload_avatar_to(instance, filename):
    filename, ext = os.path.splitext(filename)
    return os.path.join(
        "avatar_images",
        "avatar_{uuid}_{filename}{ext}".format(
            uuid=uuid.uuid4(), filename=filename, ext=ext
        ),
    )


class UserProfile(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = "M", _("Male")
        FEMALE = "F", _("Female")
        UNKNOWN = "U", _("Unknown")

    user = models.OneToOneField(
        User,
        verbose_name=_("User profile"),
        related_name="profile",
        on_delete=models.CASCADE,
    )
    birth_date = models.DateField(verbose_name=_("Birth date"), null=True, blank=True)
    gender = models.CharField(
        verbose_name=_("Gender"),
        max_length=1,
        choices=GenderChoices.choices,
        default=GenderChoices.UNKNOWN,
    )

    city = models.CharField(verbose_name=_("City"), blank=True, max_length=100)
    country = models.CharField(verbose_name=_("Country"), blank=True, max_length=100)

    height = models.PositiveIntegerField(
        verbose_name=_("Height in cm"), blank=True, null=True
    )
    weight = models.DecimalField(
        verbose_name=_("Weight in kg"),
        blank=True,
        null=True,
        max_digits=4,
        decimal_places=1,
    )

    avatar = models.ImageField(
        verbose_name=_("User avatar"),
        blank=True,
        upload_to=upload_avatar_to,
        validators=[
            FileExtensionValidator(
                allowed_extensions=app_settings.get("ALLOWED_AVATAR_EXTENSIONS")
            ),
        ],
    )

    panels = [
        FieldPanel("user"),
        FieldPanel("avatar"),
        MultiFieldPanel(
            children=[FieldPanel("gender"), FieldPanel("birth_date")],
            heading=_("Basic info"),
        ),
        MultiFieldPanel(
            children=[FieldPanel("city"), FieldPanel("country")],
            heading=_("Residential"),
        ),
        MultiFieldPanel(
            children=[FieldPanel("height"), FieldPanel("weight")],
            heading=_("Measurements"),
        ),
    ]

    def __str__(self):
        return self.user.get_username()

    class Meta:
        app_label = current_app_label
        verbose_name = _("User profile")
        verbose_name_plural = _("User profiles")

    @classmethod
    def create_for_user(cls, user):
        try:
            return cls.objects.create(user=user)
        except IntegrityError:
            return user.profile

    @classmethod
    def get_for_user(cls, user):
        try:
            cls.objects.get(user=user)
        except cls.DoesNotExist:
            return None

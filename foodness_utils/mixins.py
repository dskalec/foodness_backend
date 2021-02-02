from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class NameMixin(models.Model):
    """
    Simple mixin to add CharField `name` to a model.
    """

    name = models.CharField(verbose_name=_("Name"), max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class TitleMixin(models.Model):
    """
    Simple mixin to add CharField `title` to a model.
    """

    title = models.CharField(verbose_name=_("Title"), max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class SlugMixin(models.Model):
    """
    Simple mixin to add CharField slug to a model.
    slug_source property specifies from which model field to generate the slug.
    Defaults to name.
    """

    slug = models.SlugField(verbose_name=_("Slug"), max_length=255)

    class Meta:
        abstract = True

    @property
    def slug_source(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self.slug if self.slug else slugify(self.slug_source)

        self.slug = slugify(self.slug)

        super(SlugMixin, self).save(*args, **kwargs)


class PublishDateMixin(models.Model):
    """
    Mixin for adding fields about the objects' publication status and date.
    """

    publish_from = models.DateTimeField(
        verbose_name=_("Publish date"), null=True, blank=True, db_index=True
    )
    publish_to = models.DateTimeField(
        verbose_name=_("Publish to"), null=True, blank=True
    )
    is_published = models.BooleanField(verbose_name=_("Is published?"), default=False)

    class Meta:
        abstract = True

    @property
    def published(self):
        if not self.publish_from:
            return False

        if self.publish_to:
            return self.is_published and self.publish_from <= now() < self.publish_to
        else:
            return self.is_published and self.publish_from <= now()


class CreatedDateMixin(models.Model):
    """
    Mixin for adding fields about the model creation and change date.
    """

    created_date = models.DateTimeField(
        verbose_name=_("Created date"), auto_now_add=True
    )
    last_change = models.DateTimeField(verbose_name=_("Last change"), auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_date"]

    @property
    def modified(self):
        return self.created_date != self.last_change


class OrderMixin(models.Model):
    """
    Mixin for adding the `order` field that defaults to 0.
    """

    order = models.PositiveIntegerField(verbose_name=_("Order"), default=0)

    class Meta:
        abstract = True
        ordering = ["order"]


class GenericMixin(models.Model):
    """
    Mixin for GenericForeignKey relations.
    """

    content_type = models.ForeignKey(
        ContentType, verbose_name=_("Content type"), on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(verbose_name=_("Object ID"))
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        abstract = True
        index_together = ["content_type", "object_id"]

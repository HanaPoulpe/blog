from typing import Any

from django import http
from django.db import models as django_models
from wagtail import fields, models
from wagtail.admin import panels


class Category(models.Page):
    # Content
    logo = django_models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=django_models.SET_NULL,
        help_text="Upload a logo for the category page",
        related_name="+",
    )
    description = fields.RichTextField(
        blank=True, help_text="Description of the category"
    )

    content_panels = models.Page.content_panels + [
        panels.FieldPanel("logo"),
        panels.FieldPanel("description"),
    ]

    # Display
    def get_context(self, request: http.HttpRequest) -> dict[str, Any]:
        ctx: dict[str, Any] = super().get_context(request)
        ctx["articles"] = (
            models.Page.objects.child_of(self).live().order_by("-first_published_at")
        )

        return ctx

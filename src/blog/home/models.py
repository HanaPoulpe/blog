from typing import Any, ClassVar

from django import http
from django.db import models as django_models
from wagtail import models
from wagtail.admin import panels

from blog.content import models as content_models


class HomePage(models.Page):
    # Content
    logo = django_models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=django_models.SET_NULL,
        help_text="Upload a logo for the site homepage",
        related_name="+",
    )
    introduction = django_models.TextField(
        max_length=255, blank=True, help_text="Short site introduction"
    )

    # Editor interface
    content_panels = models.Page.content_panels + [
        panels.FieldPanel("logo"),
        panels.FieldPanel("introduction"),
    ]

    # Tree management
    subpage_types: ClassVar[list[str]] = ["content.Category"]
    parent_page_types: ClassVar[list[str]] = ["wagtailcore.Page"]

    # Context management
    def get_context(self, request: http.HttpRequest) -> dict[str, Any]:
        ctx: dict[str, Any] = super().get_context(request)
        ctx["categories"] = self.get_categories()

        return ctx

    def get_categories(self) -> django_models.QuerySet[content_models.Category]:
        categories: django_models.QuerySet[content_models.Category] = (
            content_models.Category.objects.child_of(self).live().order_by("title")
        )
        return categories

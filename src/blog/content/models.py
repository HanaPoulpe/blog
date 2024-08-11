from typing import Any, ClassVar

from django import http
from django.contrib.auth import models as auth_models
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

    @property
    def articles(self) -> django_models.QuerySet["Article"]:
        qs: django_models.QuerySet[Article] = (
            Article.objects.child_of(self).live().order_by("-first_published_at")
        )
        return qs

    @property
    def sub_categories(self) -> django_models.QuerySet["Category"]:
        qs: django_models.QuerySet[Category] = (
            Category.objects.child_of(self).live().order_by("title")
        )
        return qs

    # Display
    def get_context(self, request: http.HttpRequest) -> dict[str, Any]:
        ctx: dict[str, Any] = super().get_context(request)
        ctx["articles"] = self.articles  # TODO: pagination

        sub_categories = self.sub_categories.all()
        ctx["sub_categories"] = [
            (
                c,
                c.articles[:3],  # TODO: remove hard-coded limit
            )
            for c in sub_categories
        ]

        return ctx


class Article(models.Page):
    # Content
    logo = django_models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=django_models.SET_NULL,
        help_text="Upload a logo for the article page",
        related_name="+",
    )
    summary = django_models.CharField(
        max_length=511, blank=True, help_text="Summary of the article"
    )
    content = fields.RichTextField(blank=True, help_text="Content of the article")

    @property
    def category(self) -> Category:
        parent = self.get_parent()
        assert parent  # Articles can't be at root level
        assert isinstance(parent, Category)  # Article must be child of a Category

        return parent

    @property
    def author(self) -> auth_models.User:
        author: auth_models.User = self.owner
        return author

    content_panels = models.Page.content_panels + [
        panels.FieldPanel("logo"),
        panels.FieldPanel("summary"),
        panels.FieldPanel("content"),
    ]

    parent_page_types: ClassVar[list[str]] = ["content.Category"]

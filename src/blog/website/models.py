from django.db import models
from wagtail.contrib.settings import models as wg_settings


@wg_settings.register_setting
class BlogSettings(wg_settings.BaseGenericSetting):
    banner = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Website banner",
        related_name="+",
    )
    banner_color = models.CharField(
        max_length=9,
        null=False,
        blank=False,
        default="#000000",
        help_text="Background color of the banner.",
    )
    title_color = models.CharField(
        max_length=9,
        null=False,
        blank=False,
        default="#FFFFFF",
        help_text="Color of the site title.",
    )

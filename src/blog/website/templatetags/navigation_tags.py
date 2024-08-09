from django import template
from wagtail import models

register = template.Library()


class SiteNotFound(Exception):
    pass


@register.simple_tag(takes_context=True)
def get_site_root(context: template.Context) -> models.Page:
    root_page = models.Site.find_for_request(context.get("request", {})).root_page

    if not root_page:
        raise SiteNotFound()
    return root_page


@register.simple_tag(takes_context=True)
def get_current_page_location(context: template.Context) -> list[models.Page]:
    page: models.Page | None = context.get("page")
    home = get_site_root(context)
    if not page or page.id == home.id:
        return []

    parents = [page]

    while page := page.get_parent():
        if page.id == get_site_root(context).id:
            break

        parents.append(page)

    return parents[::-1]

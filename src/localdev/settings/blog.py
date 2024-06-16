from blog import settings

from . import base, interfaces


class BlogSite(base.Base, interfaces.Site, settings.BlogSite):
    pass

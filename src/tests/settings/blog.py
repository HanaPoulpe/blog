from blog import settings

from . import base, interfaces


class BlogSite(interfaces.InterfaceMixin, base.Base, settings.BlogSite):
    pass

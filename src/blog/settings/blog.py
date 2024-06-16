
from . import base, interfaces


class Blog(base.Base):
    pass


class BlogSite(interfaces.Site, base.Base):
    pass

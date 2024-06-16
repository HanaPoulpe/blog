from blog import settings

from . import base


class AllAppsMixin(base.Base, settings.AllAppsMixin):
    pass

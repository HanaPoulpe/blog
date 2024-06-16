import uuid
from typing import ClassVar

from blog import settings
from frozenlist import FrozenList


class Base(settings.Base):
    DEBUG: bool = True
    SECRET_KEY: ClassVar[str] = str(uuid.getnode())

    # SECURITY WARNING: define the correct hosts in production!
    ALLOWED_HOSTS: FrozenList[str] = FrozenList(["*"])

    EMAIL_BACKEND: str = "django.core.mail.backends.console.EmailBackend"

    WAGTAILADMIN_BASE_URL: str = "http://localhost:8000"

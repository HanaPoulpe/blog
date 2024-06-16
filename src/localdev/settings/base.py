import uuid
from typing import ClassVar

from blog import settings


class Base(settings.Base):
    DEBUG: bool = True
    SECRET_KEY: ClassVar[str] = str(uuid.getnode())

    # SECURITY WARNING: define the correct hosts in production!
    ALLOWED_HOSTS: list[str] = ["*"]

    EMAIL_BACKEND: str = "django.core.mail.backends.console.EmailBackend"

    WAGTAILADMIN_BASE_URL: str = "http://localhost:8000"

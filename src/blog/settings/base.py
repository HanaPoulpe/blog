import os
import pathlib
from typing import Any, ClassVar

import environs
from configurations import Configuration
from frozendict import frozendict
from frozenlist import FrozenList

env = environs.Env()


class Base(Configuration):
    # Base settings
    PROJECT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent
    BASE_DIR: pathlib.Path = PROJECT_DIR.parent

    DEBUG: bool = False

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

    # Application definition

    INSTALLED_APPS: ClassVar[list[str]] = [
        "blog.home",
        "blog.search",
        "blog.website",
        "blog.content",
        "wagtail.contrib.forms",
        "wagtail.contrib.redirects",
        "wagtail.contrib.settings",
        "wagtail.embeds",
        "wagtail.sites",
        "wagtail.users",
        "wagtail.snippets",
        "wagtail.documents",
        "wagtail.images",
        "wagtail.search",
        "wagtail.admin",
        "wagtail",
        "modelcluster",
        "taggit",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "health_check",
        "health_check.db",
        "health_check.contrib.migrations",
        "django_linear_migrations",
    ]

    MIDDLEWARE: ClassVar[list[str]] = [
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "django.middleware.security.SecurityMiddleware",
        "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    ]

    HEALTH_CHECK: ClassVar[dict[str, Any]] = {
        "SUBSETS": {
            "readiness": [
                "DatabaseBackend",
                "MigrationCheck",
            ],
            "liveness": ["DatabaseBackend"],
        },
    }

    ROOT_URLCONF: str = "blog.urls"

    TEMPLATES: FrozenList[dict] = FrozenList(
        [
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [
                    os.path.join(PROJECT_DIR, "templates"),
                ],
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.debug",
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                        "wagtail.contrib.settings.context_processors.settings",
                    ],
                },
            },
        ]
    )

    WSGI_APPLICATION: str = "blog.wsgi.application"

    # Database
    # https://docs.djangoproject.com/en/5.0/ref/settings/#databases

    DATABASES: frozendict[str, Any] = frozendict(
        {
            "default": {
                "ENGINE": "django.db.backends.postgresql_psycopg2",
                "NAME": env.str("DATABASE_NAME"),
                "USER": env.str("DATABASE_USER"),
                "PASSWORD": env.str("DATABASE_PASSWORD"),
                "HOST": env.str("DATABASE_HOST"),
                "PORT": env.int("DATABASE_PORT"),
            }
        }
    )

    # Password validation
    # https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS: FrozenList[dict[str, Any]] = FrozenList(
        [
            {
                "NAME": (
                    "django.contrib.auth.password_validation."
                    "UserAttributeSimilarityValidator"
                ),
            },
            {
                "NAME": (
                    "django.contrib.auth.password_validation.MinimumLengthValidator"
                ),
            },
            {
                "NAME": (
                    "django.contrib.auth.password_validation.CommonPasswordValidator"
                ),
            },
            {
                "NAME": (
                    "django.contrib.auth.password_validation.NumericPasswordValidator"
                ),
            },
        ]
    )

    # Internationalization
    # https://docs.djangoproject.com/en/5.0/topics/i18n/

    LANGUAGE_CODE: str = env.str("DEFAULT_LANGUAGE", "en-us")

    TIME_ZONE: str = env.str("TIME_ZONE", "UTC")

    USE_I18N: bool = True

    USE_TZ: bool = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/5.0/howto/static-files/

    STATICFILES_FINDERS: ClassVar[list[str]] = [
        "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    ]

    STATICFILES_DIRS: ClassVar[list[pathlib.Path]] = [
        PROJECT_DIR.joinpath("static"),
    ]

    STATIC_ROOT: pathlib.Path = BASE_DIR.joinpath("static")
    STATIC_URL: str = "/static/"

    MEDIA_ROOT: pathlib.Path = BASE_DIR.joinpath("media")
    MEDIA_URL: str = "/media/"

    # Default storage settings, with the staticfiles storage updated.
    # See https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-STORAGES
    STORAGES: frozendict[str, dict[str, str]] = frozendict(
        {
            "default": {
                "BACKEND": "django.core.files.storage.FileSystemStorage",
            },
            # ManifestStaticFilesStorage is recommended in production, to prevent
            # outdated JavaScript / CSS assets being served from cache
            # (e.g. after a Wagtail upgrade).
            # See https://docs.djangoproject.com/en/5.0/ref/contrib/staticfiles/#manifeststaticfilesstorage
            "staticfiles": {
                "BACKEND": (
                    "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
                ),
            },
        }
    )

    # Wagtail settings

    WAGTAIL_SITE_NAME: str = "Hana's blog"

    # Search
    # https://docs.wagtail.org/en/stable/topics/search/backends.html
    WAGTAILSEARCH_BACKENDS: ClassVar[frozendict[str, dict[str, str]]] = frozendict(
        {
            "default": {
                "BACKEND": "wagtail.search.backends.database",
            },
        }
    )

    # Base URL to use when referring to full URLs within the Wagtail admin backend -
    # e.g. in notification emails. Don't include '/admin' or a trailing slash
    WAGTAILADMIN_BASE_URL: str = env.url("BLOG_SITE_URL", "http://blog.localhost")

    # Allowed file extensions for documents in the document library.
    # This can be omitted to allow all files
    # but note that this may present a security risk
    # if untrusted users are allowed to upload files -
    # see https://docs.wagtail.org/en/stable/advanced_topics/deploying.html#user-uploaded-files
    WAGTAILDOCS_EXTENSIONS: ClassVar[FrozenList[str]] = FrozenList(
        [
            "csv",
            "docx",
            "key",
            "odt",
            "pdf",
            "pptx",
            "rtf",
            "txt",
            "xlsx",
            "zip",
        ]
    )

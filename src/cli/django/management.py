import argparse
import os
import pathlib
from typing import Any, ClassVar, TypeGuard

import manage
from cli import base


def is_str_iterable(value: Any) -> TypeGuard[list[str]]:
    return all(isinstance(item, str) for item in value)


class _Manage(base.Command):
    cwd: ClassVar[pathlib.Path] = base.PROJECT_ROOT

    django_settings: ClassVar[str] = "blog.settings"
    django_configuration: ClassVar[str] = ""
    django_command: ClassVar[str] = ""

    def add_arguments(self, parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
        parser = super().add_arguments(parser)

        parser.add_argument(
            "--settings",
            type=str,
            default=self.django_settings,
            help="Django settings module",
        )
        parser.add_argument(
            "--configuration",
            type=str,
            default=self.django_configuration,
            help="Django configuration",
        )

        return parser

    def get_django_args(
        self,
        settings: str,
        configuration: str,
        *args: Any,
        **kwargs: Any,
    ) -> list[str]:
        settings = os.environ.get(
            "DJANGO_SETTINGS_MODULE", settings or self.django_settings
        )
        configuration = os.environ.get(
            "DJANGO_CONFIGURATION", configuration or self.django_configuration
        )

        return [
            self.name,
            self.django_command,
            f"--settings={settings}",
            f"--configuration={configuration}",
        ]

    def handle(
        self,
        settings: str,
        configuration: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings or self.django_settings)
        os.environ.setdefault(
            "DJANGO_CONFIGURATION", configuration or self.django_configuration
        )

        manage.main(
            self.get_django_args(
                settings,
                configuration,
                *args,
                **kwargs,
            )
        )


class Manage(base.CommandWithParser):
    name: ClassVar[str] = "django_manage"
    description: ClassVar[str] = "Django manage.py wrapper"

    def handle(self, *args: Any, **kwargs: Any) -> None:
        assert is_str_iterable(args)

        manage.main(["manage", *args])


class RunServer(_Manage):
    name: ClassVar[str] = "django_runserver"
    description: ClassVar[str] = "Starts Django server"
    django_command: ClassVar[str] = "runserver"

    def add_arguments(self, parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
        parser = super().add_arguments(parser)

        parser.add_argument(
            "--host",
            type=str,
            default="0.0.0.0",
            help="Host to run server on",
        )
        parser.add_argument(
            "--port",
            type=int,
            default=8000,
            help="Port to run server on",
        )

        return parser

    def get_django_args(
        self,
        settings: str,
        configuration: str,
        host: str,
        port: int,
        *args: Any,
        **kwargs: Any,
    ) -> list[str]:
        django_args = super().get_django_args(
            settings,
            configuration,
            *args,
            **kwargs,
        )
        django_args.append(f"{host}:{port}")

        return django_args

    def handle(self, *args: Any, **kwargs: Any) -> None:
        print("Collecting static files...")
        CollectStaticFiles.as_command().handle(*args, **kwargs)
        super().handle(*args, **kwargs)


class MakeMigrations(_Manage):
    name: ClassVar[str] = "django_makemigrations"
    description: ClassVar[str] = "Creates Django migrations"
    django_command: ClassVar[str] = "makemigrations"


class Migrate(_Manage):
    name: ClassVar[str] = "django_migrate"
    description: ClassVar[str] = "Migrates Django database"
    django_command: ClassVar[str] = "migrate"

    django_settings: ClassVar[str] = "localdev.settings"
    django_configuration: ClassVar[str] = "AllAppsMixin"


class Shell(_Manage):
    name: ClassVar[str] = "django_shell"
    description: ClassVar[str] = "Starts Django shell"
    django_command: ClassVar[str] = "shell"

    django_configuration = "Shell"


class CreateSuperUser(_Manage):
    name: ClassVar[str] = "django_createsuperuser"
    description: ClassVar[str] = "Creates Django superuser"
    django_command: ClassVar[str] = "createsuperuser"


class CollectStaticFiles(_Manage):
    name: ClassVar[str] = "django_collectstatic"
    description: ClassVar[str] = "Collects static files"
    django_command: ClassVar[str] = "collectstatic"

    def get_django_args(
        self,
        settings: str,
        configuration: str,
        *args: Any,
        **kwargs: Any,
    ) -> list[str]:
        django_args = super().get_django_args(
            settings,
            configuration,
            *args,
            **kwargs,
        )
        django_args.append("-l")
        django_args.append("--noinput")

        return django_args

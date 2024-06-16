import argparse
import pathlib
from typing import Any, ClassVar

import manage

from scripts import base


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
        return [
            self.name,
            self.django_command,
            f"--settings={settings}",
            f"--configuration={configuration}",
        ]

    def handle(self, *args: Any, **kwargs: Any) -> None:
        manage.main(self.get_django_args(*args, **kwargs))


class Manage(base.CommandWithParser):
    name: ClassVar[str] = "django_manage"
    description: ClassVar[str] = "Django manage.py wrapper"

    def handle(self, *args: Any, **kwargs: Any) -> None:
        manage.main(*args)


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


class CreateSuperUser(_Manage):
    name: ClassVar[str] = "django_createsuperuser"
    description: ClassVar[str] = "Creates Django superuser"
    django_command: ClassVar[str] = "createsuperuser"

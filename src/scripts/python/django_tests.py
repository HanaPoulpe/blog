import pathlib
from typing import Any, ClassVar

from scripts.django import management

from . import tests


class _DjangoTests(tests.Pytest):
    django_settings_module: ClassVar[str] = "tests.settings"
    django_configuration: ClassVar[str] = ""

    collect_static: ClassVar[bool] = False

    def get_env(self, *args: Any, **kwargs: Any) -> dict[str, str]:
        env = super().get_env(*args, **kwargs)
        env["DJANGO_CONFIGURATION"] = self.django_configuration

        return env

    def handle(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        if self.collect_static:
            management.CollectStaticFiles.as_command()(
                [
                    f"--settings={self.django_settings_module}",
                    f"--configuration={self.django_configuration}",
                ]
            )

        super().handle(*args, **kwargs)


class BlogSiteTests(_DjangoTests):
    name: ClassVar[str] = "blog_site_tests"
    description: ClassVar[str] = "Runs python blog site tests"
    django_configuration: ClassVar[str] = "BlogSite"

    collect_static: ClassVar[bool] = True

    def get_default_files(self, *args: Any, **kwargs: Any) -> list[pathlib.Path | str]:
        return [
            "integration/interfaces/agnostic/**/test_*.py",
            "integration/interfaces/blog_site/**/test_*.py",
            "functional/blog/**/test_*.py",
            "unit/**/test_*.py",
        ]


class AllAppsTests(_DjangoTests):
    name: ClassVar[str] = "all_apps_tests"
    description: ClassVar[str] = "Runs python all apps tests"
    django_configuration: ClassVar[str] = "AllAppsMixin"

    collect_static: ClassVar[bool] = True

    def get_default_files(self, *args: Any, **kwargs: Any) -> list[pathlib.Path | str]:
        return [
            "functional/all_apps/**/test_*.py",
            "unit/**/test_*.py",
        ]


class UnitTests(_DjangoTests):
    name: ClassVar[str] = "unit_tests"
    description: ClassVar[str] = "Runs python unit tests"
    django_configuration: ClassVar[str] = "Base"

    def get_default_files(self, *args: Any, **kwargs: Any) -> list[pathlib.Path | str]:
        return ["unit/**/test_*.py"]


class ShellTests(_DjangoTests):
    name: ClassVar[str] = "shell_tests"
    description: ClassVar[str] = "Runs python shel tests"
    django_configuration: ClassVar[str] = "Shell"

    collect_static: ClassVar[bool] = True

    def get_default_files(self, *args: Any, **kwargs: Any) -> list[pathlib.Path | str]:
        return [
            "integration/interfaces/agnostic/**/test_*.py",
            "integration/interfaces/shell/**/test_*.py",
            "functional/blog/**/test_*.py",
            "unit/**/test_*.py",
        ]

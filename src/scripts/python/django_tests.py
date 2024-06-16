import pathlib
from typing import Any, ClassVar

from . import tests


class _DjangoTests(tests.Pytest):
    django_configuration: ClassVar[str] = ""

    def get_env(self, *args: Any, **kwargs: Any) -> dict[str, str]:
        env = super().get_env(*args, **kwargs)
        env["DJANGO_SETTINGS_MODULE"] = self.django_configuration

        return env


class BlogSiteTests(_DjangoTests):
    name: ClassVar[str] = "blog_site_tests"
    description: ClassVar[str] = "Runs python blog site tests"
    django_configuration: ClassVar[str] = "BlogSite"

    def get_default_files(self, *args: Any, **kwargs: Any) -> list[pathlib.Path | str]:
        return [
            "integrations/interfaces/agnostic/**/test_*.py",
            "integrations/interfaces/blog_site/**/test_*.py",
            "functional/blog/**/test_*.py",
            "unit/**/test_*.py",
        ]


class AllAppsTests(_DjangoTests):
    name: ClassVar[str] = "all_apps_tests"
    description: ClassVar[str] = "Runs python all apps tests"
    django_configuration: ClassVar[str] = "AllAppsMixin"

    def get_default_files(self, *args: Any, **kwargs: Any) -> list[pathlib.Path | str]:
        return [
            "functional/all_apps/**/test_*.py",
            "unit/**/test_*.py",
        ]


class UnitTests(tests.Pytest):
    name: ClassVar[str] = "unit_tests"
    description: ClassVar[str] = "Runs python unit tests"

    def get_default_files(self, *args: Any, **kwargs: Any) -> list[pathlib.Path | str]:
        return ["unit/**/test_*.py"]

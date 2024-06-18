from collections.abc import Iterable

import pytest
from blog.home import models as home_models

import tests.fixtures  # noqa: F401


@pytest.fixture(autouse=True)
def home_page(home_page: home_models.HomePage) -> home_models.HomePage:
    return home_page


def pytest_collection_modifyitems(items: Iterable[pytest.Item]) -> None:
    for item in items:
        item.add_marker("django_db")

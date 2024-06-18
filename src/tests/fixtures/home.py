import pytest
from blog.home import models

from tests.factories import home


@pytest.fixture
def home_page() -> models.HomePage:
    return home.HomePageFactory()

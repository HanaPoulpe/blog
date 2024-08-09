import pytest
from blog.home import models
from wagtail import models as wagtail_models

from tests.factories import home


@pytest.fixture
def home_page() -> models.HomePage:
    home_pg = home.HomePageFactory()

    site = wagtail_models.Site.objects.first()
    site.root_page = home_pg
    site.save()

    return home_pg

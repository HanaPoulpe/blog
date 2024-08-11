import pytest
from django.contrib.auth import models as auth_models

from tests.factories import auth as auth_factory


@pytest.fixture
def user() -> auth_models.User:
    return auth_factory.UserFactory()

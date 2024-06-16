import os.path

import dotenv
import pytest

from tests.fixtures import *  # noqa: F403


def pytest_runtest_setup(item: pytest.Item) -> None:
    dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

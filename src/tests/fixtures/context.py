import pytest
from django import http, template


@pytest.fixture
def request_context() -> template.Context:
    request = http.HttpRequest()
    request.META = {
        "HTTP_HOST": "testserver",
        "SERVER_PORT": "8000",
    }

    return template.Context(
        {
            "request": request,
        }
    )

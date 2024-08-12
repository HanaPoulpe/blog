from blog.home import models as home_models
from django import test as django_test


class TestHomePage:
    def test_render(
        self,
        home_page: home_models.HomePage,
        client: django_test.Client,
    ) -> None:
        response = client.get("/")

        assert response.status_code == 200

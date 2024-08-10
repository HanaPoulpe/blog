import attrs
import pytest
from blog.content import models as content_models
from django import http

from tests.factories import category as category_factory


@pytest.fixture
def category() -> content_models.Category:
    return category_factory.CategoryFactory()


class TestCategory:
    @attrs.frozen(slots=True)
    class CategoryRequest:
        category: content_models.Category
        request: http.HttpRequest

    @pytest.fixture
    def request_for_category(self, category: content_models.Category) -> CategoryRequest:
        request = http.HttpRequest()

        request.method = "GET"
        request.path = category.slug

        return self.CategoryRequest(category=category, request=request)

    def test_get_context_empty(self, request_for_category: CategoryRequest) -> None:
        ctx = request_for_category.category.get_context(request_for_category.request)

        assert "articles" in ctx
        articles_list = list(ctx["articles"])
        assert articles_list == []

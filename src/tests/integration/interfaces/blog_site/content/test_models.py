import random

import attrs
import pytest
from django import http
from django import test as django_test
from django.contrib.auth import models as auth_models

from blog.content import models as content_models
from tests import utils as test_utils
from tests.factories import content as content_factory


@pytest.fixture
def category() -> content_models.Category:
    return content_factory.CategoryFactory()


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

        assert "sub_categories" in ctx
        sub_categories_list = list(ctx["sub_categories"])
        assert sub_categories_list == []

    @pytest.fixture
    def category_with_children(
        self, request: pytest.FixtureRequest, category: content_models.Category
    ) -> CategoryRequest:
        articles, sub_categories = request.param

        for _ in range(articles):
            content_factory.ArticleFactory(parent=category)

        for _ in range(sub_categories):
            child_category = content_factory.CategoryFactory(parent=category)
            for _ in range(random.randint(0, 5)):
                content_factory.ArticleFactory(parent=child_category)

        http_request = http.HttpRequest()

        http_request.method = "GET"
        http_request.path = category.slug

        return self.CategoryRequest(category=category, request=http_request)

    @pytest.mark.parametrize(
        "category_with_children",
        [(1, 0), (0, 1), (1, 1)],
        ids=["articles only", "subcategories only", "both articles and subcategories"],
        indirect=["category_with_children"],
    )
    def test_get_context_with_children(
        self, category_with_children: CategoryRequest
    ) -> None:
        ctx = category_with_children.category.get_context(category_with_children.request)

        assert "articles" in ctx
        articles_list = list(ctx["articles"])
        assert len(articles_list) == category_with_children.category.articles.count()

        assert "sub_categories" in ctx
        sub_categories_list = list(ctx["sub_categories"])
        assert (
            len(sub_categories_list)
            == category_with_children.category.sub_categories.count()
        )
        for sub_category, sub_articles in sub_categories_list:
            assert len(sub_articles) == min(sub_category.articles.count(), 3)

    def test_render(
        self,
        category: content_models.Category,
        client: django_test.Client,
    ) -> None:
        response = client.get(category.get_url())

        assert response.status_code == 200


class TestArticles:
    @pytest.fixture
    def article(
        self, category: content_models.Category, user: auth_models.User
    ) -> content_models.Article:
        return content_factory.ArticleFactory(
            parent=category,
            owner=user,
        )

    def test_category(self, article: content_models.Article) -> None:
        category = article.category

        assert article in category.articles

    def test_author(self, article: content_models.Article) -> None:
        author = article.author

        assert author is not None
        assert author == article.owner

    def test_render(
        self, article: content_models.Article, client: django_test.Client
    ) -> None:
        response = client.get(test_utils.get_full_page_path(article))

        assert response.status_code == 200

import pytest
from django import template

from blog.home import models
from blog.website.templatetags import navigation_tags
from tests.factories import home as home_factories


class TestGetSiteRoot:
    def test_get_site_root(
        self,
        home_page: models.HomePage,
        request_context: template.Context,
    ) -> None:
        site_root = navigation_tags.get_site_root(request_context)

        assert site_root.id == home_page.id


class TestGetCurrentPageLocation:
    @pytest.fixture
    def home_page_context(
        self,
        home_page: models.HomePage,
        request_context: template.Context,
    ) -> template.Context:
        request_context.dicts["page"] = home_page

        return request_context

    @pytest.fixture
    def subpage_context(
        self,
        request: pytest.FixtureRequest,
        home_page: models.HomePage,
        request_context: template.Context,
    ) -> template.Context:
        depth = request.param

        page = home_page
        for _ in range(depth):
            page = home_factories.HomePageFactory(parent=page)

        request_context.dicts.append({"page": page})
        return request_context

    @pytest.mark.parametrize(
        "depth,subpage_context",
        [(i, i) for i in range(0, 4)],
        ids=["home", *[f"subpage {i}" for i in range(1, 4)]],
        indirect=["subpage_context"],
    )
    def test_subpage(self, depth: int, subpage_context: template.Context) -> None:
        current_page_location = navigation_tags.get_current_page_location(subpage_context)

        assert len(current_page_location) == depth

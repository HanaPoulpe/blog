import factory
import wagtail_factories

from blog.content import models


class CategoryFactory(wagtail_factories.PageFactory):
    class Meta:
        model = models.Category

    title = factory.Sequence(lambda n: f"Category {n}")


class ArticleFactory(wagtail_factories.PageFactory):
    class Meta:
        model = models.Article

    title = factory.Sequence(lambda n: f"Article {n}")

    parent = factory.SubFactory(CategoryFactory)

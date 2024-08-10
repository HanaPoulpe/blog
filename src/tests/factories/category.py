import wagtail_factories
from blog.content import models


class CategoryFactory(wagtail_factories.PageFactory):
    class Meta:
        model = models.Category

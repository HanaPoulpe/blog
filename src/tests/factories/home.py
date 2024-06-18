import wagtail_factories
from blog.home import models


class HomePageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = models.HomePage

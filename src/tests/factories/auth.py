import factory
import faker
from django.contrib.auth import models
from factory import django as django_factory

fake = faker.Faker()


class UserFactory(django_factory.DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.lazy_attribute(lambda x: fake.user_name)

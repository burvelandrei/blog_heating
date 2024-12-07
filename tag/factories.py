import factory
from .models import Tag

class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Faker('word')
    description = factory.Faker('text')
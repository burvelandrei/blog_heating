import factory
from .models import Comment
from publication.factories import PublicationFactory
from user.factories import CustomUserFactory

class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    publication = factory.SubFactory(PublicationFactory)
    content = factory.Faker('paragraph')
    author = factory.SubFactory(CustomUserFactory)
import factory
from factory.django import DjangoModelFactory
from .models import Article, Video, Publication
from django.contrib.contenttypes.models import ContentType

class ArticleFactory(DjangoModelFactory):
    class Meta:
        model = Article

    title = factory.Faker('sentence', nb_words=4)
    content = factory.Faker('text')
    category = factory.SubFactory('category.factories.CategoryFactory')
    author = factory.SubFactory('user.factories.CustomUserFactory')

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)

class VideoFactory(DjangoModelFactory):
    class Meta:
        model = Video

    title = factory.Faker('sentence', nb_words=4)
    youtube_url = factory.Faker('url')
    category = factory.SubFactory('category.factories.CategoryFactory')
    author = factory.SubFactory('user.factories.CustomUserFactory')

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)

class PublicationFactory(DjangoModelFactory):
    class Meta:
        model = Publication

    title = factory.Faker('sentence', nb_words=4)
    content_type = factory.LazyAttribute(lambda o: ContentType.objects.get_for_model(o.content_object))
    object_id = factory.SelfAttribute('content_object.id')

    @factory.lazy_attribute
    def content_object(self):
        return ArticleFactory()
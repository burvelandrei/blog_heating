import random
import factory
import io
from factory import post_generation
from factory.django import DjangoModelFactory
from .models import Article, Video, Publication
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from PIL import Image

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

    @post_generation
    def image(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.image = extracted
        else:
            # Создаем случайное изображение
            image = Image.new('RGB', (100, 100), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            image_io = io.BytesIO()
            image.save(image_io, format='JPEG')
            image_file = ContentFile(image_io.getvalue())
            self.image.save(f'article_{self.id}.jpg', image_file)

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
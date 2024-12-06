from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from category.models import Category
from tag.models import Tag
# Create your models here.

class TimeStappedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Publication(TimeStappedModel):
    title = models.CharField(max_length=255, null=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Article(models.Model):
    title = models.CharField(max_length=255, null=False)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    publications = GenericRelation(Publication, related_query_name='article')
    tags = models.ManyToManyField(Tag, related_name='articles')


class Video(models.Model):
    title = models.CharField(max_length=255, null=False)
    youtube_url = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='videos')
    publications = GenericRelation(Publication, related_query_name='video')
    tags = models.ManyToManyField(Tag, related_name='videos')
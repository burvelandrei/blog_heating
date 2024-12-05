from django.db import models
from category.models import Category
# Create your models here.

class TimeStappedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Publication(TimeStappedModel):
    title = models.CharField(max_length=255, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='publications')

    class Meta:
        abstract = True


class Article(Publication):
    article = models.TextField()


class Video(Publication):
    video = models.URLField()
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from category.models import Category
from user.models import CustomUser
from tag.models import Tag


class TimeStappedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата публикации")

    class Meta:
        abstract = True


class Publication(models.Model):
    title = models.CharField(max_length=255, blank=True, verbose_name="Наименование")
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name="Тип публикации"
    )
    object_id = models.PositiveIntegerField(verbose_name="ID контента")
    content_object = GenericForeignKey("content_type", "object_id")
    publisched_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации"
    )

    def save(self, *args, **kwargs):
        # Устанавливаем title на основе связанного объекта
        if self.content_object:
            self.title = self.content_object.title
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


class Article(TimeStappedModel):
    title = models.CharField(max_length=255, null=False, verbose_name="Наименование")
    content = models.TextField(verbose_name="Текст статьи")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="articles",
        verbose_name="Категория",
    )
    publications = GenericRelation(Publication, related_query_name="article")
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="publications"
    )
    tags = models.ManyToManyField(
        Tag, related_name="articles", null=True, blank=True, verbose_name="Теги"
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Video(TimeStappedModel):
    title = models.CharField(max_length=255, null=False, verbose_name="Наименование")
    youtube_url = models.URLField(verbose_name="Ссылка на youtube видео")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="videos",
        verbose_name="Категория",
    )
    publications = GenericRelation(Publication, related_query_name="video")
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="publications"
    )
    tags = models.ManyToManyField(
        Tag, related_name="videos", null=True, blank=True, verbose_name="Теги"
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Видеоролик'
        verbose_name_plural = 'Видеоролики'

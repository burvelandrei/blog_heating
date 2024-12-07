from django.db import models
from publication.models import Publication
from user.models import CustomUser


class TimeStappedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата публикации")

    class Meta:
        abstract = True


class Comment(TimeStappedModel):
    publication = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Публикация",
    )
    content = models.TextField(verbose_name="Содержание")
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )

    def __str__(self):
        return f"Comment on {self.publication.title}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

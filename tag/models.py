from django.db import models

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=20, null=False, verbose_name="Наименование")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
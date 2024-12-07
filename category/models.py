from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, verbose_name="Наименование")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
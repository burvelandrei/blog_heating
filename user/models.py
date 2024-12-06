from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Дополнительные поля
    birth_date = models.DateField(null=True, blank=True)
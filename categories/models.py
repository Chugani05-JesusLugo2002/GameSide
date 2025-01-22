from colorfield.fields import ColorField
from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    color = ColorField(blank=True)

    def __str__(self):
        return self.name

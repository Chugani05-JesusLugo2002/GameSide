from colorfield.fields import ColorField
from django.db import models


class Platform(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(unique=True)
    description = models.CharField(blank=True)
    color = ColorField(blank=True)

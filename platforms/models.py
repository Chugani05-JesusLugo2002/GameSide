from django.db import models


class Platform(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(unique=True)
    description = models.CharField(blank=True)
    logo = models.ImageField(blank=True, null=True)

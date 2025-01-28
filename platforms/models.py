from django.db import models


class Platform(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(blank=True, null=True, default='logos/default.jpg')

    def __str__(self):
        return self.name

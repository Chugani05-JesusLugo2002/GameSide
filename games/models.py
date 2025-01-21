from django.db import models


class Game(models.Model):
    class Pegi(models.IntegerChoices):
        PEGI3 = 3, 'PEGI 3'
        PEGI7 = 7, 'PEGI 7'
        PEGI12 = 12, 'PEGI 12'
        PEGI16 = 16, 'PEGI 16'
        PEGI18 = 18, 'PEGI 18'

    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    cover = models.ImageField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.PositiveIntegerField()
    released_at = models.DateField()
    pegi = models.PositiveSmallIntegerField(choices=Pegi)
    category = models.ForeignKey(
        'categories.Category', on_delete=models.PROTECT, related_name='games'
    )
    platforms = models.ManyToManyField('platforms.Platform', related_name='games')

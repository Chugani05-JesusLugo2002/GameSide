from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
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
        'categories.Category',
        on_delete=models.SET_NULL,
        related_name='games',
        null=True,
        blank=True,
    )
    platforms = models.ManyToManyField('platforms.Platform', related_name='games')

    def __str__(self):
        return self.title


class Review(models.Model):
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f'{self.user} - {self.game}'

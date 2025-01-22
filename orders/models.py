from django.db import models
from django.contrib.auth import get_user_model


class Order(models.Model):
    class Status(models.IntegerChoices):
        INITIATED = 0
        CONFIRMED = 1
        CANCELLED = 2
        PAID = 3
    
    status = models.PositiveSmallIntegerField(choices=Status)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    key = models.UUIDField(null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders')
    games = models.ManyToManyField('games.Game', related_name='orders')
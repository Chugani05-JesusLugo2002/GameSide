from django.db import models
from django.contrib.auth import get_user_model
import uuid


class Order(models.Model):
    class Status(models.IntegerChoices):
        INITIATED = 1
        CONFIRMED = 2
        PAID = 3
        CANCELLED = -1
    
    status = models.IntegerField(choices=Status, default=Status.INITIATED)
    key = models.UUIDField(null=True, blank=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders')
    games = models.ManyToManyField('games.Game', related_name='orders', blank=True)

    @property
    def price():
        return 'hola, soy el price'
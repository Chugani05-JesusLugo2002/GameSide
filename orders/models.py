import uuid

from django.contrib.auth import get_user_model
from django.db import models

from games.models import Game


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
    def price(self):
        return sum((float(game.price) for game in self.games.all()))

    def confirm(self):
        self.status = Order.Status.CONFIRMED
        self.save()

    def cancel(self):
        self.status = Order.Status.CANCELLED
        for game_ordered in self.games.all():
            game = Game.objects.get(pk=game_ordered.pk)
            game.stock += 1
            game.save()
        self.save()

    def pay(self):
        self.status = Order.Status.PAID
        self.save()

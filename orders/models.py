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

        @property
        def valid_choices(self):
            return 

    status = models.IntegerField(choices=Status, default=Status.INITIATED)
    key = models.UUIDField(null=True, blank=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders')
    games = models.ManyToManyField('games.Game', related_name='orders', blank=True)

    @property
    def price(self):
        return sum((float(game.price) for game in self.games.all()))
    
    def add_game(self, game):
        self.games.add(game)
        game.stock -= 1

    def change_status(self, status_value):
        match status_value:
            case Order.Status.CONFIRMED:
                resolution = self.confirm()
            case Order.Status.CANCELLED:
                resolution = self.cancel()
        return resolution

    def confirm(self):
        self.status = Order.Status.CONFIRMED
        self.save()
        return {'status': self.get_status_display()}

    def cancel(self):
        self.status = Order.Status.CANCELLED
        for game_ordered in self.games.all():
            game = Game.objects.get(pk=game_ordered.pk)
            game.stock += 1
            game.save()
        self.save()
        return {'status': self.get_status_display()}

    def pay(self) -> dict:
        self.status = Order.Status.PAID
        self.save()
        return {'status': self.get_status_display(), 'key': self.key}

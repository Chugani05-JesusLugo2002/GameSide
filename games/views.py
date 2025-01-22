from django.core import serializers
from django.http import HttpResponse

from .models import Game, Review


def game_list(request):
    games = Game.objects.all()
    data = serializers.serialize('json', games)
    return HttpResponse(data)


def game_detail(request, game_slug):
    game = Game.objects.get(slug=game_slug)
    data = serializers.serialize('json', game)
    return HttpResponse(data)


def review_list(request, game_slug):
    game = Game.objects.get(slug=game_slug)
    reviews = game.reviews.all()
    data = serializers.serialize('json', reviews)
    return HttpResponse(data)


def review_detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    data = serializers.serialize('json', review)
    return HttpResponse(data)


def add_review(request, game_slug):
    game = Game.objects.get(slug=game_slug)
    return HttpResponse()

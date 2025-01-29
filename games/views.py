from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer


def game_list(request):
    games = Game.objects.all()
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


def game_detail(request, game_slug):
    game = Game.objects.get(slug=game_slug)
    serializer = GameSerializer(game, request=request)
    return serializer.json_response()


def review_list(request, game_slug):
    game = Game.objects.get(slug=game_slug)
    reviews = game.reviews.all()
    serializer = ReviewSerializer(reviews, request=request)
    return serializer.json_response()


def review_detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    serializer = ReviewSerializer(review, request=request)
    return serializer.json_response()


def add_review(request, game_slug):
    pass

from django.views.decorators.csrf import csrf_exempt

from shared.utils import assert_method

from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer
from .utils import assert_game_found, assert_review_found


@assert_method('GET')
def game_list(request):
    games = Game.objects.all()
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


@assert_method('GET')
@assert_game_found
def game_detail(request, game_slug):
    game = Game.objects.get(slug=game_slug)
    serializer = GameSerializer(game, request=request)
    return serializer.json_response()


@assert_method('GET')
@assert_game_found
def review_list(request, game_slug):
    game = Game.objects.get(slug=game_slug)
    reviews = game.reviews.all()
    serializer = ReviewSerializer(reviews, request=request)
    return serializer.json_response()


@assert_method('GET')
@assert_review_found
def review_detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    serializer = ReviewSerializer(review, request=request)
    return serializer.json_response()


@csrf_exempt
@assert_method('POST')
@assert_game_found
def add_review(request, game_slug):
    pass

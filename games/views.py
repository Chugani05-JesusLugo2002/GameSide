from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.utils import assert_json_body, assert_method, assert_required_fields, assert_token

from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer
from .utils import assert_game_found, assert_review_found


@assert_method('GET')
def game_list(request):
    # TODO: Filter with querystring
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
@assert_json_body
@assert_required_fields('token', 'rating', 'comment')
@assert_token
@assert_game_found
def add_review(request, game_slug):
    rating = request.data['rating']
    comment = request.data['comment']
    game = Game.objects.get(slug=game_slug)

    if not 1 < rating <= 5:
        return JsonResponse({'error': 'Rating is out of range'}, status=400)
    review = Review.objects.create(
        comment=comment, rating=rating, game=game, author=request.token.user
    )
    return JsonResponse({'id': review.pk})

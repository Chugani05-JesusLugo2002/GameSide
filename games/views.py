from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import (
    assert_method,
    assert_object_found,
    assert_token,
    get_valid_json_fields,
)

from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer


@assert_method('GET')
def game_list(request: HttpRequest) -> JsonResponse:
    games = Game.objects.all()
    if category_query := request.GET.get('category'):
        games = games.filter(category__slug=category_query)
    if platform_query := request.GET.get('platform'):
        games = games.filter(platforms__slug=platform_query)
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


@assert_method('GET')
@assert_object_found(Game, with_slug=True)
def game_detail(request: HttpRequest, game_slug: str) -> JsonResponse:
    game = Game.objects.get(slug=game_slug)
    serializer = GameSerializer(game, request=request)
    return serializer.json_response()


@assert_method('GET')
@assert_object_found(Game, with_slug=True)
def review_list(request: HttpRequest, game_slug: str) -> JsonResponse:
    game = Game.objects.get(slug=game_slug)
    reviews = game.reviews.all()
    serializer = ReviewSerializer(reviews, request=request)
    return serializer.json_response()


@assert_method('GET')
@assert_object_found(Review)
def review_detail(request: HttpRequest, review_pk: int) -> JsonResponse:
    review = Review.objects.get(pk=review_pk)
    serializer = ReviewSerializer(review, request=request)
    return serializer.json_response()


@csrf_exempt
@assert_method('POST')
@get_valid_json_fields('rating', 'comment')
@assert_token
@assert_object_found(Game, with_slug=True)
def add_review(request: HttpRequest, game_slug: str) -> JsonResponse:
    rating = request.data['rating']
    if not 1 < rating <= 5:
        return JsonResponse({'error': 'Rating is out of range'}, status=400)
    comment = request.data['comment']
    game = Game.objects.get(slug=game_slug)
    review = Review.objects.create(
        comment=comment, rating=rating, game=game, author=request.token.user
    )
    return JsonResponse({'id': review.pk})

from django.http import JsonResponse
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
def game_list(request):
    category_query = request.GET.get('category')
    platform_query = request.GET.get('platform')
    games = Game.objects.all()
    if category_query:
        games = games.filter(category__slug=category_query)
    if platform_query:
        games = games.filter(platforms__slug=platform_query)
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


@assert_method('GET')
@assert_object_found(Game, with_slug=True)
def game_detail(request, game_slug):
    game = Game.objects.get(slug=game_slug)
    serializer = GameSerializer(game, request=request)
    return serializer.json_response()


@assert_method('GET')
@assert_object_found(Game, with_slug=True)
def review_list(request, game_slug):
    game = Game.objects.get(slug=game_slug)
    reviews = game.reviews.all()
    serializer = ReviewSerializer(reviews, request=request)
    return serializer.json_response()


@assert_method('GET')
@assert_object_found(Review)
def review_detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    serializer = ReviewSerializer(review, request=request)
    return serializer.json_response()


@csrf_exempt
@assert_method('POST')
@get_valid_json_fields('rating', 'comment')
@assert_token
@assert_object_found(Game, with_slug=True)
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

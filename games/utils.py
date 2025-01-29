from django.http import JsonResponse

from .models import Game, Review


def assert_game_found(func):
    def wrapper(*args, **kwargs):
        game_slug = kwargs['game_slug']
        try:
            Game.objects.get(slug=game_slug)
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found'}, status=404)
        return func(*args, **kwargs)

    return wrapper


def assert_review_found(func):
    def wrapper(*args, **kwargs):
        review_pk = kwargs['review_pk']
        try:
            Review.objects.get(pk=review_pk)
        except Review.DoesNotExist:
            return JsonResponse({'error': 'Review not found'}, status=404)
        return func(*args, **kwargs)

    return wrapper

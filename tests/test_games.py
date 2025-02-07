import uuid

import pytest
from model_bakery import baker

from games.models import Game, Review
from platforms.models import Platform

from .helpers import (
    compare_games,
    compare_reviews,
    get_json,
    post_json,
)

# ==============================================================================
# GAMES
# ==============================================================================


@pytest.mark.django_db
def test_game_list(client):
    baker.make(Game, _fill_optional=True, _quantity=10)
    for game in (games := Game.objects.all()):
        game.platforms.set(baker.make(Platform, _fill_optional=True, _quantity=3))
    status, response = get_json(client, '/api/games/')
    assert status == 200
    for game in response:
        compare_games(game, games.get(pk=game['id']))


@pytest.mark.django_db
def test_game_list_fails_when_method_is_not_allowed(client):
    status, response = post_json(client, '/api/games/')
    assert status == 405
    assert response == {'error': 'Method not allowed'}


@pytest.mark.django_db
def test_game_list_with_querystring_filter(client, category, platform):
    blacklist_games = baker.make(Game, _fill_optional=True, _quantity=10)
    baker.make(Game, category=category, _fill_optional=True, _quantity=10)
    games = Game.objects.filter(category=category, platforms=platform)
    for game in (games := Game.objects.all()):
        game.platforms.add(platform)
    status, response = get_json(
        client, f'/api/games/?category={category.slug}&platform={platform.slug}'
    )
    assert status == 200
    for game in response:
        compare_games(game, games.get(pk=game['id']))
    blacklist_games_pks = [game.pk for game in blacklist_games]
    for game in response:
        assert game['id'] not in blacklist_games_pks


@pytest.mark.django_db
def test_game_list_with_querystring_filter_fails_when_method_is_not_allowed(client):
    status, response = post_json(
        client, '/api/games/?category=category-test&platform=platform-test'
    )
    assert status == 405
    assert response == {'error': 'Method not allowed'}


@pytest.mark.django_db
def test_game_detail(client, game):
    status, response = get_json(client, f'/api/games/{game.slug}/')
    assert status == 200
    compare_games(response, game)


@pytest.mark.django_db
def test_game_detail_fails_when_method_is_not_allowed(client):
    status, response = post_json(client, '/api/games/test/')
    assert status == 405
    assert response == {'error': 'Method not allowed'}


@pytest.mark.django_db
def test_game_detail_fails_when_game_does_not_exist(client):
    status, response = get_json(client, '/api/games/test/')
    assert status == 404
    assert response == {'error': 'Game not found'}


# ==============================================================================
# REVIEWS
# ==============================================================================


@pytest.mark.django_db
def test_review_list(client, game):
    baker.make(Review, game=game, _fill_optional=True, _quantity=10)
    reviews = Review.objects.filter(game=game)
    status, response = get_json(client, f'/api/games/{game.slug}/reviews/')
    assert status == 200
    for review in response:
        compare_reviews(review, reviews.get(pk=review['id']))


@pytest.mark.django_db
def test_review_list_fails_when_method_is_not_allowed(client):
    status, response = post_json(client, '/api/games/test/reviews/')
    assert status == 405
    assert response == {'error': 'Method not allowed'}


@pytest.mark.django_db
def test_review_list_fails_when_game_does_not_exist(client):
    status, response = get_json(client, '/api/games/test/reviews/')
    assert status == 404
    assert response == {'error': 'Game not found'}


@pytest.mark.django_db
def test_review_detail(client, game, review):
    review.game = game
    review.save()
    status, response = get_json(client, f'/api/games/reviews/{review.pk}/')
    assert status == 200
    compare_reviews(response, review)


@pytest.mark.django_db
def test_review_detail_fails_when_method_is_not_allowed(client):
    status, response = post_json(client, '/api/games/reviews/1/')
    assert status == 405
    assert response == {'error': 'Method not allowed'}


@pytest.mark.django_db
def test_review_detail_fails_when_review_does_not_exist(client):
    status, response = get_json(client, '/api/games/reviews/1/')
    assert status == 404
    assert response == {'error': 'Review not found'}


@pytest.mark.django_db
def test_add_review(client, token, game):
    user = token.user
    game.user = user
    game.save()
    data = {'rating': 5, 'comment': 'This is a test comment'}
    status, response = post_json(client, f'/api/games/{game.slug}/reviews/add/', data, token.key)
    assert status == 200
    assert response == {'id': 1}
    review = Review.objects.get(pk=response['id'])
    assert review.rating == data['rating']
    assert review.comment == data['comment']
    assert review.game == game
    assert review.author == user


@pytest.mark.django_db
def test_add_review_fails_when_json_body_is_invalid(client):
    status, response = post_json(client, '/api/games/test/reviews/add/', '{')
    assert status == 400
    assert response == {'error': 'Invalid JSON body'}


@pytest.mark.django_db
def test_add_review_fails_when_token_is_invalid(client):
    data = {'rating': 1, 'comment': 'This is a test comment'}
    status, response = post_json(client, '/api/games/test/reviews/add/', data, 'invalid-token')
    assert status == 400
    assert response == {'error': 'Invalid authentication token'}


@pytest.mark.django_db
def test_add_review_fails_when_missing_required_fields(client):
    status, response = post_json(client, '/api/games/test/reviews/add/', '{}')
    assert status == 400
    assert response == {'error': 'Missing required fields'}


@pytest.mark.django_db
def test_add_review_fails_when_rating_is_out_of_range(client, token, game):
    data = {'rating': 6, 'comment': 'This is a test comment'}
    status, response = post_json(client, f'/api/games/{game.slug}/reviews/add/', data, token.key)
    assert status == 400
    assert response == {'error': 'Rating is out of range'}


@pytest.mark.django_db
def test_add_review_fails_when_unregistered_token(client):
    data = {'rating': 1, 'comment': 'This is a test comment'}
    status, response = post_json(client, '/api/games/test/reviews/add/', data, str(uuid.uuid4()))
    assert status == 401
    assert response == {'error': 'Unregistered authentication token'}


@pytest.mark.django_db
def test_add_review_fails_when_game_not_found(client, token):
    data = {'rating': 1, 'comment': 'This is a test comment'}
    status, response = post_json(client, '/api/games/test/reviews/add/', data, token.key)
    assert status == 404
    assert response == {'error': 'Game not found'}

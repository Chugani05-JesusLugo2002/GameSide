import pytest

from users.models import Token

from .helpers import get_json, post_json


@pytest.mark.django_db
def test_auth(client, token):
    user = token.user
    user.set_password('test')
    user.save()
    data = {'username': user.username, 'password': 'test'}
    status, response = post_json(client, '/api/auth/', data)
    assert status == 200
    assert Token.objects.get(user=user, key=response['token'])


@pytest.mark.django_db
def test_auth_fails_when_invalid_json_body(client):
    status, response = post_json(client, '/api/auth/', '{"token": "}')
    assert status == 400
    assert response == {'error': 'Invalid JSON body'}


@pytest.mark.django_db
def test_auth_fails_when_missing_required_fields(client):
    status, response = post_json(client, '/api/auth/')
    assert status == 400
    assert response == {'error': 'Missing required fields'}


@pytest.mark.django_db
def test_auth_fails_when_invalid_credentials(client, token):
    user = token.user
    data = {'username': user.username, 'password': 'invalid'}
    status, response = post_json(client, '/api/auth/', data)
    assert status == 401
    assert response == {'error': 'Invalid credentials'}


@pytest.mark.django_db
def test_auth_fails_when_method_is_not_allowed(client):
    status, response = get_json(client, '/api/auth/')
    assert status == 405
    assert response == {'error': 'Method not allowed'}

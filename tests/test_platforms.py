import pytest
from model_bakery import baker

from platforms.models import Platform

from .helpers import compare_platforms, get_json, post_json


@pytest.mark.django_db
def test_platform_list(client):
    baker.make(Platform, _fill_optional=True, _quantity=10)
    platforms = Platform.objects.all()
    status, response = get_json(client, '/api/platforms/')
    assert status == 200
    for platform in response:
        compare_platforms(platform, platforms.get(pk=platform['id']))


@pytest.mark.django_db
def test_platform_list_fails_when_method_is_not_allowed(client):
    status, response = post_json(client, '/api/platforms/')
    assert status == 405
    assert response == {'error': 'Method not allowed'}


@pytest.mark.django_db
def test_platform_detail(client, platform):
    status, response = get_json(client, f'/api/platforms/{platform.slug}/')
    assert status == 200
    compare_platforms(response, platform)


@pytest.mark.django_db
def test_platform_detail_fails_when_method_is_not_allowed(client):
    status, response = post_json(client, '/api/platforms/test/')
    assert status == 405
    assert response == {'error': 'Method not allowed'}


@pytest.mark.django_db
def test_platform_detail_fails_when_platform_does_not_exist(client):
    status, response = get_json(client, '/api/platforms/test/')
    assert status == 404
    assert response == {'error': 'Platform not found'}

import pytest
from model_bakery import baker

from categories.models import Category

from .helpers import compare_categories, get_json, post_json


@pytest.mark.django_db
def test_category_list(client):
    baker.make(Category, _fill_optional=True, _quantity=10)
    categories = Category.objects.all()
    status, response = get_json(client, '/api/categories/')
    assert status == 200
    for category in response:
        compare_categories(category, categories.get(pk=category['id']))


@pytest.mark.django_db
def test_category_list_fails_when_method_is_not_allowed(client):
    status, response = post_json(client, '/api/categories/')
    assert status == 405
    assert response == {'error': 'Method not allowed'}


@pytest.mark.django_db
def test_category_detail(client, category):
    status, response = get_json(client, f'/api/categories/{category.slug}/')
    assert status == 200
    compare_categories(response, category)


@pytest.mark.django_db
def test_category_detail_fails_when_method_is_not_allowed(client):
    status, _ = post_json(client, '/api/categories/test/')
    assert status == 405


@pytest.mark.django_db
def test_category_detail_fails_when_category_does_not_exist(client):
    status, response = get_json(client, '/api/categories/test/')
    assert status == 404
    assert response == {'error': 'Category not found'}

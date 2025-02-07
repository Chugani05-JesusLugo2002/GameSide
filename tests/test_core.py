import re

import pytest
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from model_bakery import baker

from categories.models import Category
from games.models import Game, Review
from orders.models import Order
from platforms.models import Platform
from users.models import Token


@pytest.mark.django_db
def test_required_apps_are_installed():
    PROPER_APPS = ('shared', 'games', 'platforms', 'categories', 'orders', 'users')

    custom_apps = [app for app in settings.INSTALLED_APPS if not app.startswith('django')]
    for app in PROPER_APPS:
        app_config = f'{app}.apps.{app.title()}Config'
        assert app_config in custom_apps, (
            f'La aplicación <{app}> no está "creada/instalada" en el proyecto.'
        )
    assert len(custom_apps) >= len(PROPER_APPS), (
        'El número de aplicaciones propias definidas en el proyecto no es correcto.'
    )


@pytest.mark.django_db
def test_game_model_has_proper_fields():
    PROPER_FIELDS = (
        'title',
        'slug',
        'description',
        'cover',
        'price',
        'stock',
        'released_at',
        'pegi',
        'category',
        'platforms',
    )
    for field in PROPER_FIELDS:
        assert getattr(Game, field) is not None, f'El campo <{field}> no está en el modelo Game.'


@pytest.mark.django_db
def test_review_model_has_proper_fields():
    PROPER_FIELDS = ('rating', 'comment', 'game', 'author', 'created_at', 'updated_at')
    for field in PROPER_FIELDS:
        assert getattr(Review, field) is not None, (
            f'El campo <{field}> no está en el modelo Review.'
        )


@pytest.mark.django_db
def test_category_model_has_proper_fields():
    PROPER_FIELDS = ('name', 'slug', 'description', 'color')
    for field in PROPER_FIELDS:
        assert getattr(Category, field) is not None, (
            f'El campo <{field}> no está en el modelo Category.'
        )


@pytest.mark.django_db
def test_platform_model_has_proper_fields():
    PROPER_FIELDS = ('name', 'slug', 'description', 'logo')
    for field in PROPER_FIELDS:
        assert getattr(Platform, field) is not None, (
            f'El campo <{field}> no está en el modelo Platform.'
        )


@pytest.mark.django_db
def test_order_model_has_proper_fields():
    PROPER_FIELDS = ('status', 'key', 'user', 'games', 'created_at', 'updated_at')
    for field in PROPER_FIELDS:
        assert getattr(Order, field) is not None, f'El campo <{field}> no está en el modelo Order.'


@pytest.mark.django_db
def test_token_model_has_proper_fields():
    PROPER_FIELDS = ('user', 'key', 'created_at')
    for field in PROPER_FIELDS:
        assert getattr(Token, field) is not None, f'El campo <{field}> no está en el modelo Token.'


@pytest.mark.django_db
def test_order_class_has_price_property():
    assert getattr(Order, 'price')


@pytest.mark.django_db
def test_review_model_has_proper_validators():
    validators = Review.rating.field.validators
    assert len(validators) == 2, (
        'Debe haber dos validadores (min y max) para el campo "rating" de Review.'
    )
    if 'less' in validators[0].message:
        max_validator = validators[0]
        min_validator = validators[1]
    else:
        min_validator = validators[0]
        max_validator = validators[1]
    assert isinstance(min_validator, MinValueValidator)
    assert isinstance(max_validator, MaxValueValidator)
    assert min_validator.limit_value == 1
    assert max_validator.limit_value == 5


@pytest.mark.django_db
def test_game_category_is_null_when_category_is_deleted(category, game):
    game.category = category
    game.save()
    category.delete()
    game.refresh_from_db()
    assert game.category is None


@pytest.mark.django_db
def test_enum_fields_have_proper_choices():
    choices = Game.pegi.field.choices
    assert choices == [
        (3, 'Pegi3'),
        (7, 'Pegi7'),
        (12, 'Pegi12'),
        (16, 'Pegi16'),
        (18, 'Pegi18'),
    ], 'Las opciones del campo pegi(Game) no son correctas.'

    choices = Order.status.field.choices
    assert choices == [
        (1, 'Initiated'),
        (2, 'Confirmed'),
        (3, 'Paid'),
        (-1, 'Cancelled'),
    ], 'Las opciones del campo status(Order) no son correctas.'


@pytest.mark.django_db
def test_model_default_values():
    game = baker.make(Game)
    assert game.cover == 'covers/default.jpg'
    category = baker.make(Category)
    assert category.color == '#ffffff'
    platform = baker.make(Platform)
    assert platform.logo == 'logos/default.jpg'
    order = baker.make(Order)
    assert order.status == 1
    assert re.fullmatch(r'[a-f0-9\-]+', str(order.key), re.IGNORECASE)
    token = baker.make(Token)
    assert re.fullmatch(r'[a-f0-9\-]+', str(token.key), re.IGNORECASE)


@pytest.mark.django_db
def test_models_are_available_on_admin(admin_client):
    MODELS = (
        'games.Game',
        'games.Review',
        'categories.Category',
        'platforms.Platform',
        'orders.Order',
        'users.Token',
    )

    for model in MODELS:
        url_model_path = model.replace('.', '/').lower()
        url = f'/admin/{url_model_path}/'
        response = admin_client.get(url)
        assert response.status_code == 200, f'El modelo <{model}> no está habilitado en el admin.'

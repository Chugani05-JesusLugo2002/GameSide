import pytest
from django.contrib.auth.models import User
from model_bakery import baker


@pytest.fixture
def user():
    return baker.make(User, _fill_optional=True)


@pytest.fixture
def token():
    return baker.make('users.Token', _fill_optional=True)


@pytest.fixture
def order():
    return baker.make('orders.Order', _fill_optional=True)


@pytest.fixture
def game():
    return baker.make('games.Game', _fill_optional=True)


@pytest.fixture
def category():
    return baker.make('categories.Category', _fill_optional=True)


@pytest.fixture
def platform():
    return baker.make('platforms.Platform', _fill_optional=True)


@pytest.fixture
def review():
    return baker.make('games.Review', _fill_optional=True)

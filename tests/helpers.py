from datetime import datetime
from urllib.parse import urljoin

BASE_URL = 'http://testserver/'


def build_url(url: str) -> str:
    return urljoin(BASE_URL, url)


def datetime_isoformats_are_close(dtiso1: str, dtiso2: str = '') -> bool:
    dt1 = datetime.fromisoformat(dtiso1)
    dt2 = datetime.fromisoformat(dtiso2) if dtiso2 else datetime.now()
    return abs((dt1 - dt2).total_seconds()) < 1


def compare_categories(rcategory, ecategory) -> None:
    # rcategory: response-category
    # ecategory: expected-category
    assert rcategory['id'] == ecategory.pk
    assert rcategory['name'] == ecategory.name
    assert rcategory['slug'] == ecategory.slug
    assert rcategory['description'] == ecategory.description
    assert rcategory['color'] == ecategory.color


def compare_platforms(rplatform, eplatform) -> None:
    # rplatform: response-platform
    # eplatform: expected-platform
    assert rplatform['id'] == eplatform.pk
    assert rplatform['name'] == eplatform.name
    assert rplatform['slug'] == eplatform.slug
    assert rplatform['description'] == eplatform.description
    assert rplatform['logo'] == build_url(eplatform.logo.url)


def compare_games(rgame, egame) -> None:
    # rgame: response-game
    # egame: expected-game
    assert rgame['id'] == egame.pk
    assert rgame['title'] == egame.title
    assert rgame['slug'] == egame.slug
    assert rgame['cover'] == build_url(egame.cover.url)
    assert rgame['price'] == float(egame.price)
    assert rgame['stock'] == egame.stock
    assert rgame['released_at'] == egame.released_at.isoformat()
    assert rgame['pegi'] == egame.get_pegi_display()
    assert rgame['category']['id'] == egame.category.pk
    assert rgame['category']['name'] == egame.category.name
    assert rgame['category']['slug'] == egame.category.slug
    assert rgame['category']['description'] == egame.category.description
    assert rgame['category']['color'] == egame.category.color
    for rplatform, eplatform in zip(rgame['platforms'], egame.platforms.all()):
        compare_platforms(rplatform, eplatform)


def compare_users(ruser, euser) -> None:
    # ruser: response-user
    # euser: expected-user
    assert ruser['id'] == euser.pk
    assert ruser['username'] == euser.username
    assert ruser['email'] == euser.email
    assert ruser['first_name'] == euser.first_name
    assert ruser['last_name'] == euser.last_name


def compare_reviews(rreview, ereview) -> None:
    # rreview: response-review
    # ereview: expected-review
    assert rreview['id'] == ereview.pk
    assert rreview['rating'] == ereview.rating
    assert rreview['comment'] == ereview.comment
    compare_games(rreview['game'], ereview.game)
    compare_users(rreview['author'], ereview.author)
    assert datetime_isoformats_are_close(rreview['created_at'], ereview.created_at.isoformat())
    assert datetime_isoformats_are_close(rreview['updated_at'], ereview.updated_at.isoformat())


def get_json(client, url: str) -> tuple:
    response = client.get(url)
    return response.status_code, response.json()


def post_json(client, url: str, data: dict = {}) -> tuple:
    response = client.post(url, data, content_type='application/json')
    return response.status_code, response.json()

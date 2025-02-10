from django.http import HttpRequest, JsonResponse

from shared.decorators import assert_method, assert_object_found

from .models import Category
from .serializers import CategorySerializer


@assert_method('GET')
def category_list(request: HttpRequest) -> JsonResponse:
    categories = Category.objects.all()
    serializer = CategorySerializer(categories)
    return serializer.json_response()


@assert_method('GET')
@assert_object_found(Category, with_slug=True)
def category_detail(request: HttpRequest, category_slug: str) -> JsonResponse:
    category = Category.objects.get(slug=category_slug)
    serializer = CategorySerializer(category)
    return serializer.json_response()

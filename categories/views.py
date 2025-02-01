from shared.decorators import assert_method, assert_object_found

from .models import Category
from .serializers import CategorySerializer


@assert_method('GET')
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories)
    return serializer.json_response()


@assert_method('GET')
@assert_object_found(Category, with_slug=True)
def category_detail(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    serializer = CategorySerializer(category)
    return serializer.json_response()

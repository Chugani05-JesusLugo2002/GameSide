from shared.utils import assert_method

from .models import Category
from .serializers import CategorySerializer
from .utils import assert_object_found


@assert_method('GET')
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories)
    return serializer.json_response()


@assert_method('GET')
@assert_object_found
def category_detail(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    serializer = CategorySerializer(category)
    return serializer.json_response()

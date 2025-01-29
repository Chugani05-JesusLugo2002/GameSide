from .models import Category
from .serializers import CategorySerializer


def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories)
    return serializer.json_response()


def category_detail(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    serializer = CategorySerializer(category)
    return serializer.json_response()

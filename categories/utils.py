from django.http import JsonResponse

from .models import Category


def assert_category_found(func):
    def wrapper(*args, **kwargs):
        category_slug = kwargs['category_slug']
        try:
            Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)
        return func(*args, **kwargs)
    return wrapper

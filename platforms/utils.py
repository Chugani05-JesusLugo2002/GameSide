from django.http import JsonResponse

from .models import Platform


def assert_object_found(func):
    def wrapper(*args, **kwargs):
        platform_slug = kwargs['platform_slug']
        try:
            Platform.objects.get(slug=platform_slug)
        except Platform.DoesNotExist:
            return JsonResponse({'error': 'Platform not found'}, status=404)
        return func(*args, **kwargs)

    return wrapper

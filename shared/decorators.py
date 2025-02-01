import json
from django.http import JsonResponse

from users.models import Token


def assert_method(method: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            request = args[0]
            if request.method != method:
                return JsonResponse({'error': 'Method not allowed'}, status=405)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def assert_object_found(model, *, with_slug = False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            model_name = model.__name__
            suffix = '_slug' if with_slug else '_pk'
            instance_id = model_name.lower() + suffix
            try:
                if with_slug:
                    model.objects.get(slug=kwargs[instance_id])
                else:
                    model.objects.get(pk=kwargs[instance_id])
            except model.DoesNotExist:
                return JsonResponse({'error': f'{model_name} not found'}, status=404)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def get_valid_json_fields(*fields: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            request = args[0]
            try:
                request.data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON body'}, status=400)
            body_fields = request.data.keys()
            for field in fields:
                if field not in body_fields:
                    return JsonResponse({'error': 'Missing required fields'}, status=400)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def assert_token(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        token = request.data['token']
        try:
            request.token = Token.objects.get(key=token)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Unknown authentication token'}, status=401)
        return func(*args, **kwargs)
    return wrapper

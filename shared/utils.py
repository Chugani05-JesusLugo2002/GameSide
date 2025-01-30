import json

from django.http import JsonResponse


def assert_method(method: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            request = args[0]
            if request.method != method:
                return JsonResponse({'error': 'Method not allowed'}, status=405)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def assert_json_body(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        try:
            request.data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)
        return func(*args, **kwargs)
    return wrapper


def assert_required_fields(*fields):
    def decorator(func):
        def wrapper(*args, **kwargs):
            request = args[0]
            if len(fields) != len(request.data.keys()):
                return JsonResponse({'error': 'Missing required fields'}, status=400) 
            for field, key in zip(fields, request.data.keys()):
                if field != key:
                    return JsonResponse({'error': 'Missing required fields'}, status=400)
            return func(*args, **kwargs)
        return wrapper
    return decorator
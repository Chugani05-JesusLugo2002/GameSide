from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

from shared.utils import assert_method, assert_json_body, assert_required_fields


@csrf_exempt
@assert_method('POST')
@assert_json_body
@assert_required_fields('username', 'password')
def auth(request):
    username = request.data['username']
    password = request.data['password']
    if user := authenticate(request, username=username, password=password):
        return JsonResponse({'token': user.token.key})
    return JsonResponse({'error': 'Invalid credentials'}, status=401)

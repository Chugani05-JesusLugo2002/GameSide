import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.utils import assert_method, assert_json_body, assert_required_fields


@csrf_exempt
@assert_method('POST')
@assert_json_body
@assert_required_fields('username', 'password')
def auth(request):
    return JsonResponse(request.data)

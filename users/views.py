import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.utils import assert_method


@csrf_exempt
@assert_method('POST')
def auth(request):
    data = json.loads(request.body)
    print(data)
    return JsonResponse(data)

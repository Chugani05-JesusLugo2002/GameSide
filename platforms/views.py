from django.http import HttpRequest, JsonResponse

from shared.decorators import assert_method, assert_object_found

from .models import Platform
from .serializers import PlatformSerializer


@assert_method('GET')
def platform_list(request: HttpRequest) -> JsonResponse:
    platforms = Platform.objects.all()
    serializer = PlatformSerializer(platforms, request=request)
    return serializer.json_response()


@assert_method('GET')
@assert_object_found(Platform, with_slug=True)
def platform_detail(request: HttpRequest, platform_slug: str) -> JsonResponse:
    platform = Platform.objects.get(slug=platform_slug)
    serializer = PlatformSerializer(platform, request=request)
    return serializer.json_response()

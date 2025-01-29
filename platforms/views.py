from shared.utils import assert_method

from .models import Platform
from .serializers import PlatformSerializer
from .utils import assert_object_found


@assert_method('GET')
def platform_list(request):
    platforms = Platform.objects.all()
    serializer = PlatformSerializer(platforms, request=request)
    return serializer.json_response()


@assert_method('GET')
@assert_object_found
def platform_detail(request, platform_slug):
    platform = Platform.objects.get(slug=platform_slug)
    serializer = PlatformSerializer(platform, request=request)
    return serializer.json_response()

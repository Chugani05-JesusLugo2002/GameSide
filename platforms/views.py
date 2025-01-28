from django.http import HttpResponse

from .models import Platform

from .serializers import PlatformSerializer


def platform_list(request):
    platforms = Platform.objects.all()
    serializer = PlatformSerializer(platforms, request=request)
    return serializer.json_response()


def platform_detail(request, platform_slug):
    platform = Platform.objects.get(slug=platform_slug)
    serializer = PlatformSerializer(platform, request=request)
    return serializer.json_response()

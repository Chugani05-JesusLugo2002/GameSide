from django.http import HttpResponse

from .models import Platform


def platform_list(request):
    platforms = Platform.objects.all()
    return HttpResponse()


def platform_detail(request, platform_slug):
    platform = Platform.objects.get(slug=platform_slug)
    return HttpResponse()

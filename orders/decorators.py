from django.http import JsonResponse

from .models import Order


def assert_owner(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        order_pk = kwargs['order_pk']
        order = Order.objects.get(pk=order_pk)
        if request.token.user != order.user:
            return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)
        return func(*args, **kwargs)
    return wrapper
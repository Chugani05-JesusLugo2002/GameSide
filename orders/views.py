from django.http import HttpResponse

from .models import Order

def add_order(request):
    pass


def order_detail(request, order_pk):
    order = Order.objects.get(pk=order_pk)
    return HttpResponse()


def confirm_order(request, order_pk):
    pass


def cancel_order(request, order_pk):
    pass


def pay_order(request, order_pk):
    pass

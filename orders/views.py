from django.http import HttpResponse

from .models import Order
from .serializers import OrderSerializer

def add_order(request):
    pass


def order_detail(request, order_pk):
    order = Order.objects.get(pk=order_pk)
    serializer = OrderSerializer(order, request=request)
    return serializer.json_response()


def confirm_order(request, order_pk):
    pass


def cancel_order(request, order_pk):
    pass


def pay_order(request, order_pk):
    pass

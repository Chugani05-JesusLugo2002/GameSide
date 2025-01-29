from django.views.decorators.csrf import csrf_exempt

from shared.utils import assert_method

from .models import Order
from .serializers import OrderSerializer


@csrf_exempt
@assert_method('POST')
def add_order(request):
    pass


@assert_method('GET')
def order_detail(request, order_pk):
    order = Order.objects.get(pk=order_pk)
    serializer = OrderSerializer(order, request=request)
    return serializer.json_response()


@csrf_exempt
@assert_method('POST')
def confirm_order(request, order_pk):
    pass


@csrf_exempt
@assert_method('POST')
def cancel_order(request, order_pk):
    pass


@csrf_exempt
@assert_method('POST')
def pay_order(request, order_pk):
    pass

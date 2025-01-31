from django.http import JsonResponse
from datetime import datetime
import re

from .models import Order


class Card():
    def __init__(self, card_number: str, exp_date: str, cvc: str):
        self.card_number = card_number
        self.exp_date = exp_date
        self.cvc = cvc

    def validate(self) -> dict|None:
        if (error := self.check_card_number()):
            return error
        if (error := self.check_exp_date()):
            return error
        if (error := self.check_cvc()):
            return error
        return None

    def check_card_number(self) -> dict|None:
        PATTERN = r'^(\d{4}\-){3}\d{4}$'
        if re.match(PATTERN, self.card_number) is None:
            return {'error': 'Invalid card number'}
        return None

    def check_exp_date(self) -> dict|None:
        PATTERN = r'^\d{2}/\d{4}$'
        if re.match(PATTERN, self.exp_date) is None:
            return {'error': 'Invalid expiration date'}
        exp_date = datetime.strptime(self.exp_date, '%m/%Y')
        if exp_date < datetime.now():
            return {'error': 'Card expired'}
        return None

    def check_cvc(self) -> dict|None:
        PATTERN = r'^\d{3}$'
        if re.match(PATTERN, self.cvc) is None:
            return {'error': 'Invalid CVC'}
        return None


def assert_order_found(func):
    def wrapper(*args, **kwargs):
        order_pk = kwargs['order_pk']
        try:
            Order.objects.get(pk=order_pk)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        return func(*args, **kwargs)

    return wrapper


def assert_owner(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        order_pk = kwargs['order_pk']
        order = Order.objects.get(pk=order_pk)
        if request.token.user != order.user:
            return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)
        return func(*args, **kwargs)

    return wrapper
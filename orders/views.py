from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from games.models import Game
from games.serializers import GameSerializer
from shared.decorators import (
    assert_method,
    assert_object_found,
    assert_token,
    get_valid_json_fields,
)
from users.models import Token

from .decorators import assert_owner
from .models import Order
from .serializers import OrderSerializer
from .utils import Card


@csrf_exempt
@assert_method('POST')
@assert_token
def add_order(request):
    token = Token.objects.get(key=request.token.key)
    order = Order.objects.create(user=token.user)
    return JsonResponse({'id': order.pk})


@csrf_exempt
@assert_method('GET')
@assert_token
@assert_object_found(Order)
@assert_owner
def order_detail(request, order_pk):
    order = Order.objects.get(pk=order_pk)
    serializer = OrderSerializer(order, request=request)
    return serializer.json_response()


@csrf_exempt
@assert_method('GET')
@assert_token
@assert_object_found(Order)
@assert_owner
def order_game_list(request, order_pk):
    games = Order.objects.get(pk=order_pk).games.all()
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


@csrf_exempt
@assert_method('POST')
@get_valid_json_fields('game-slug')
@assert_object_found(Order)
@assert_object_found(Game, with_slug=True, json_inserted=True)
@assert_token
@assert_owner
def add_game_to_order(request, order_pk):
    game = Game.objects.get(slug=request.data['game-slug'])
    if game.stock == 0:
        return JsonResponse({'error': 'Game out of stock'}, status=400)
    order = Order.objects.get(pk=order_pk)
    order.add_game(game)
    return JsonResponse({'num-games-in-order': order.games.count()})


@csrf_exempt
@assert_method('POST')
@get_valid_json_fields('status')
@assert_token
@assert_object_found(Order)
@assert_owner
def change_order_status(request, order_pk):
    order = Order.objects.get(pk=order_pk)
    status = request.data['status']
    valid_status_values = (Order.Status.CANCELLED, Order.Status.CONFIRMED)
    if status not in valid_status_values:
        return JsonResponse({'error': 'Invalid status'}, status=400)
    if order.status != Order.Status.INITIATED:
        return JsonResponse({'error': 'Orders can only be confirmed/cancelled when initiated'}, status=400)
    resolution = order.change_status(status)
    return JsonResponse(resolution)
    


@csrf_exempt
@assert_method('GET')
@assert_token
@assert_object_found(Order)
@assert_owner
def confirm_order(request, order_pk):
    order = Order.objects.get(pk=order_pk)
    if order.status != Order.Status.INITIATED:
        return JsonResponse({'error': 'Orders can only be confirmed when initiated'}, status=400)
    resolution = order.confirm()
    return JsonResponse(resolution)


@csrf_exempt
@assert_method('GET')
@assert_token
@assert_object_found(Order)
@assert_owner
def cancel_order(request, order_pk):
    order = Order.objects.get(pk=order_pk)
    if order.status != Order.Status.INITIATED:
        return JsonResponse({'error': 'Orders can only be cancelled when initiated'}, status=400)
    resolution = order.cancel()
    return JsonResponse(resolution)


@csrf_exempt
@assert_method('POST')
@get_valid_json_fields('card-number', 'exp-date', 'cvc')
@assert_token
@assert_object_found(Order)
@assert_owner
def pay_order(request, order_pk):
    card_number = request.data['card-number']
    exp_date = request.data['exp-date']
    cvc = request.data['cvc']

    card = Card(card_number, exp_date, cvc)
    if error := card.validate():
        return JsonResponse(error, status=400)

    order = Order.objects.get(pk=order_pk)
    if order.status != Order.Status.CONFIRMED:
        return JsonResponse({'error': 'Orders can only be paid when confirmed'}, status=400)
    resolution = order.pay()
    return JsonResponse(resolution)

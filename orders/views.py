from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from games.models import Game
from games.serializers import GameSerializer
from shared.decorators import assert_json_body, assert_method, assert_required_fields, assert_token, assert_object_found
from users.models import Token

from .models import Order
from .serializers import OrderSerializer
from .utils import Card
from .decorators import assert_owner


@csrf_exempt
@assert_method('POST')
@assert_json_body
@assert_required_fields('token')
@assert_token
def add_order(request):
    token = Token.objects.get(key=request.token.key)
    order = Order.objects.create(user=token.user)
    return JsonResponse({'id': order.pk})


@csrf_exempt
@assert_method('POST')
@assert_json_body
@assert_required_fields('token')
@assert_token
@assert_object_found(Order)
@assert_owner
def order_detail(request, order_pk):
    order = Order.objects.get(pk=order_pk)
    serializer = OrderSerializer(order, request=request)
    return serializer.json_response()


@csrf_exempt
@assert_method('POST')
@assert_json_body
@assert_required_fields('token')
@assert_token
@assert_object_found(Order)
@assert_owner
def order_game_list(request, order_pk):
    games = Order.objects.get(pk=order_pk).games.all()
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


@csrf_exempt
@assert_method('POST')
@assert_object_found(Order)
@assert_object_found(Game, with_slug=True)
@assert_json_body
@assert_required_fields('token')
@assert_token
@assert_owner
def add_game_to_order(request, order_pk, game_slug):
    game = Game.objects.get(slug=game_slug)
    if game.stock == 0:
        return JsonResponse({'error': 'Game out of stock'}, status=400)
    order = Order.objects.get(pk=order_pk)
    order.games.add(game)
    game.stock -= 1
    return JsonResponse({'num-games-in-order': order.games.count()})


@csrf_exempt
@assert_method('POST')
@assert_json_body
@assert_required_fields('token')
@assert_token
@assert_object_found(Order)
@assert_owner
def confirm_order(request, order_pk):
    order = Order.objects.get(pk=order_pk)
    if order.status != Order.Status.INITIATED:
        return JsonResponse({'error': 'Orders can only be confirmed when initiated'}, status=400)
    order.confirm()
    return JsonResponse({'status': order.get_status_display()})


@csrf_exempt
@assert_method('POST')
@assert_json_body
@assert_required_fields('token')
@assert_token
@assert_object_found(Order)
@assert_owner
def cancel_order(request, order_pk):
    order = Order.objects.get(pk=order_pk)
    if order.status != Order.Status.INITIATED:
        return JsonResponse({'error': 'Orders can only be cancelled when initiated'}, status=400)
    order.cancel()
    return JsonResponse({'status': order.get_status_display()})


@csrf_exempt
@assert_method('POST')
@assert_json_body
@assert_required_fields('token', 'card-number', 'exp-date', 'cvc')
@assert_token
@assert_object_found(Order)
@assert_owner
def pay_order(request, order_pk):
    card_number = request.data['card-number']
    exp_date = request.data['exp-date']
    cvc = request.data['cvc']

    card = Card(card_number, exp_date, cvc)
    if (error := card.validate()):
        return JsonResponse(error, status=400)
    
    order = Order.objects.get(pk=order_pk)
    if order.status != Order.Status.CONFIRMED:
        return JsonResponse({'error': 'Orders can only be paid when confirmed'}, status=400)
    order.pay()

    return JsonResponse({'status': order.get_status_display(), 'key': order.key})

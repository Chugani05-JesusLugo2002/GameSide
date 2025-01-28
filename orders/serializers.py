from shared.serializers import BaseSerializer

from games.serializers import GameSerializer

from .models import Order

class OrderSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'status': instance.status,
            'key': instance.key if instance.status == Order.Status.PAID else None,
            'games': GameSerializer(instance.games.all(), request=self.request),
            'created_at': instance.created_at,
            'update_at': instance.updated_at,
            # 'price': instance.price
        }
from shared.serializers import BaseSerializer

from platforms.serializers import PlatformSerializer
from categories.serializers import CategorySerializer
from users.serializers import UserSerializer


class GameSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'title': instance.title,
            'slug': instance.slug,
            'description': instance.description,
            'cover': self.build_url(instance.cover.url),
            'price': float(instance.price),
            'stock': instance.stock,
            'released_at': instance.released_at,
            'pegi': instance.pegi,
            'category': CategorySerializer(instance.category),
            'platforms': PlatformSerializer(instance.platforms.all(), request=request)
        }


class ReviewSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'comment': instance.comment,
            'rating': instance.rating,
            'game': GameSerializer(instance.game, request=request),
            'author': UserSerializer(instance.user),
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        }
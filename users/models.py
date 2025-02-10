from django.db import models
from django.conf import settings
import uuid

class Token(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key = models.UUIDField(unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
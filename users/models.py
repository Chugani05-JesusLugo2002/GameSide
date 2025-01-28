from django.db import models
from django.contrib.auth import get_user_model
import uuid

class Token(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    key = models.UUIDField(unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
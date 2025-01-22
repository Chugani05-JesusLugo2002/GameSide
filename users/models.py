from django.db import models
from django.contrib.auth import get_user_model

class Token(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    key = models.UUIDField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
from django.contrib import admin

from .models import Game, Review


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

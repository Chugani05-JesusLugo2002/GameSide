from django.contrib import admin

from .models import Game, Review


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock', 'category', 'pegi')
    list_filter = ('platforms', 'category')
    empty_value_display = 'No category available'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'game', 'rating')
    list_filter = ('author', 'game', 'rating')

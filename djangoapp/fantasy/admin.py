from django.contrib import admin
from .models import *


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'admin']

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'league', 'default_position']


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ['id', 'league', 'played']


@admin.register(LeagueRule)
class LeagueRule(admin.ModelAdmin):
    list_display = ['id', 'title', 'number', 'league', 'midfield_points', 'forward_points', 'defender_points', 'keeper_points']


@admin.register(PlayerPoints)
class PlayerPointsAdmin(admin.ModelAdmin):
    list_display = ['id', 'rule__title', 'player__name', 'round__number', 'points']


@admin.register(PlayerRoundPosition)
class PlayerRoundPosition(admin.ModelAdmin):
    list_display = ['id', 'player__name', 'round__number', 'position']

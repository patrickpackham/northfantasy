from django.contrib import admin
from .models import *

# TODO Flesh these out.

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    pass


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    pass


@admin.register(LeagueRule)
class LeagueRule(admin.ModelAdmin):
    pass


@admin.register(PlayerPoints)
class PlayerPointsAdmin(admin.ModelAdmin):
    pass


@admin.register(PlayerRoundPosition)
class PlayerRoundPosition(admin.ModelAdmin):
    pass

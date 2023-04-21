from .models import League, Round, LeagueRule
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist


class AdminCheckMixin(object):
    def dispatch(self, *args, **kwargs):
        league = League.objects.get(name__icontains=self.kwargs["league_name"])
        if self.request.user != league.admin:
            return HttpResponseRedirect(
                reverse("league_home", kwargs={"league_name": kwargs["league_name"]})
            )
        return super(AdminCheckMixin, self).dispatch(*args, **kwargs)


class ContextMixin(object):
    league = None
    round = None

    def dispatch(self, *args, **kwargs):
        try:
            if "league_name" in self.kwargs.keys():
                self.league = League.objects.get(name=self.kwargs["league_name"])
            if "round_number" in self.kwargs.keys():
                self.round = Round.objects.get(
                    league=self.league, number=self.kwargs["round_number"]
                )
            if "rule_number" in self.kwargs.keys():
                self.rule = LeagueRule.objects.get(
                    league=self.league, number=self.kwargs["rule_number"]
                )
        except ObjectDoesNotExist:
            return HttpResponseNotFound("<h1>404 - Page not found</h1>")
        return super(ContextMixin, self).dispatch(*args, **kwargs)

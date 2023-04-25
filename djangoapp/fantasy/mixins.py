from .models import League, Round, LeagueRule
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist


class AdminCheckMixin(object):
    """Simple authorization mixin for making sure only admins are editing scores."""
    def dispatch(self, *args, **kwargs):
        league = League.objects.get(name__icontains=self.kwargs["league_name"])
        if self.request.user != league.admin:
            return HttpResponseRedirect(
                reverse("league_home", kwargs={"league_name": kwargs["league_name"]})
            )
        return super(AdminCheckMixin, self).dispatch(*args, **kwargs)


class ContextMixin(object):
    """
    This class is used to provide some common variables to itself based on what is
    present in the url pattern. This mixin should only be used with views that require
    frequent use of the records named in the url used to access them.
    """
    league = None
    round = None
    rule = None

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

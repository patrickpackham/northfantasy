from django.views.generic import TemplateView, FormView, ListView
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.forms import modelformset_factory

from .forms import BasePlayerPointsFormSet, PlayerPositionsFormSet, PlayerPointsForm
from .models import Player, Round, LeagueRule, PlayerPoints
from .mixins import AdminCheckMixin, ContextMixin


class LeagueHome(ContextMixin, ListView):
    template_name = "league_home.html"
    model = Player

    def get_context_data(self):
        context = super(LeagueHome, self).get_context_data()
        context["league"] = self.league
        return context

    def get_queryset(self):
        return sorted(
            Player.objects.filter(league=self.league),
            key=lambda a: a.points(),
            reverse=True,
        )


class Rounds(ContextMixin, ListView):
    template_name = "rounds.html"
    model = Round

    def get_context_data(self):
        context = super(Rounds, self).get_context_data()
        context["league"] = self.league
        return context

    def get_queryset(self):
        return Round.objects.filter(league=self.league)


class RoundDetail(ContextMixin, ListView):
    template_name = "round_detail.html"
    model = Player

    def get_queryset(self):
        qs = sorted(
            Player.objects.filter(league=self.league),
            key=lambda a: a.points(round=self.round),
            reverse=True,
        )
        return qs

    def get_context_data(self, **kwargs):
        context = super(RoundDetail, self).get_context_data(**kwargs)
        context["league"] = self.league
        context["round"] = self.round
        return context


class PlayerPositionsView(AdminCheckMixin, ContextMixin, FormView):
    template_name = "add_positions.html"
    form_class = PlayerPositionsFormSet

    def get_context_data(self, **kwargs):
        context = super(PlayerPositionsView, self).get_context_data(**kwargs)
        context["round"] = self.round
        context["league"] = self.league
        return context

    def get_success_url(self):
        kwargs = self.kwargs
        kwargs["round_number"] = 1
        kwargs["rule_number"] = 1
        return reverse("add_points", kwargs=kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["round"] = self.round
        return kwargs

    def form_valid(self, form):
        for subform in form:
            subform.save()
        return super(PlayerPositionsView, self).form_valid(form)


class PlayerPointsView(AdminCheckMixin, ContextMixin, TemplateView):
    template_name = "add_points.html"
    success_url = "/success/"
    model = PlayerPoints
    form_class = PlayerPointsForm
    formset_class = BasePlayerPointsFormSet

    def get_context_data(self, **kwargs):
        context = super(PlayerPointsView, self).get_context_data(**kwargs)
        context["league"] = self.league
        context["rule"] = self.rule
        context["form"] = self.get_form()
        context["players"] = Player.objects.filter(league=self.league)
        return context

    def get_form(self):
        initial = self.get_initial()
        kwargs = self.get_form_kwargs()

        # See the get_formset_class docstring for how
        # to customize the formset on a per-view basis
        if self.request.method == "POST":
            formset = self.get_formset_class(extra=self.rule.required_extra_forms)(
                data=self.request.POST,
                rule=self.rule,
                form_kwargs=kwargs,
                empty_initial=initial,
            )
        else:
            formset = self.get_formset_class(extra=self.rule.required_extra_forms)(
                rule=self.rule, form_kwargs=kwargs, empty_initial=initial
            )
            # Only set initial if there is no instance, so we don't override record data
            for form in formset:
                if not form.instance.id:
                    form.initial = initial

        return formset

    def get_initial(self):
        initial = {"round": self.round, "rule": self.rule, "points": 0}
        return initial

    def get_form_kwargs(self):
        # Set the round qs for the form to be only the value sanitized for this URL.
        round_qs = Round.objects.filter(id=self.round.id)
        kwargs = {"league": self.league, "round": round_qs, "rule": self.rule}
        return kwargs

    def get_formset_class(self, extra=1):
        """
        Instead of passing a formset class already assembled by a factory,
        we can use this method to override the defaults on a per-view basis.
        In this case, some rules might need more or less additional forms, so we can
        override the extra parameter to this method.
        Add more custom parameters here if you want to.
        """
        return modelformset_factory(
            self.model,
            form=self.form_class,
            formset=self.formset_class,
            extra=extra,
            fields=["id", "player", "round", "rule", "points"],
        )

    def post(self, request, *args, **kwargs):
        # We don't really need granular control of invalid and valid behaviour here as
        # users shouldn't be able to submit bad data to via the form to this method.
        form = self.get_form()
        for subform in form:
            if subform.is_valid():
                subform.save()
            elif subform.instance.id and not subform.data.get("player"):
                subform.instance.delete()
        messages.success(self.request, "Scores successfully updated!")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        next_rule = (
            LeagueRule.objects.filter(league=self.league, number__gt=self.rule.number)
            .order_by("id")
            .first()
        )
        if next_rule:
            return reverse(
                "add_points",
                kwargs={
                    "league_name": self.league.name,
                    "round_id": self.round.number,
                    "rule_id": next_rule.number,
                },
            )
        return reverse(
            "round_detail",
            kwargs={"league_name": self.league.name, "round_number": self.round.number},
        )

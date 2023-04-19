from django.views.generic import TemplateView, FormView, ListView
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.forms import modelformset_factory

from .forms import PlayerPointsFormSet, PlayerPositionsFormSet, \
    PlayerPointsForm
from .models import League, Player, Round, LeagueRule, PlayerPoints
from .auth import AdminCheckMixin


# todo Make a an object that assigns self.league, round, etc base don what's
# todo available in the kwargs. Make each of the below clases use this mixin.


class LeagueHome(ListView):
    template_name = 'league_home.html'
    model = Player

    def get_context_data(self):
        context = super(LeagueHome, self).get_context_data()
        context['league'] = League.objects.get(
            name__icontains=self.kwargs['league_name'])
        return context

    def get_queryset(self):
        return sorted(Player.objects.filter(
            league__name__icontains=self.kwargs['league_name']
        ), key=lambda a: a.points(), reverse=True)


class Rounds(ListView):
    template_name = 'rounds.html'
    model = Round

    def get_context_data(self):
        context = super(Rounds, self).get_context_data()
        context['league'] = League.objects.get(
            name__icontains=self.kwargs['league_name'])
        return context

    def get_queryset(self):
        return Round.objects.filter(
            league__name__icontains=self.kwargs['league_name'])


class RoundDetail(ListView):
    template_name = 'round_detail.html'
    model = Player

    def get_queryset(self):
        round = Round.objects.get(
            league__name__icontains=self.kwargs['league_name'],
            number=self.kwargs['round_number']
        )
        qs = sorted(Player.objects.filter(
            league__name__icontains=self.kwargs['league_name']
        ), key=lambda a: a.points(round=round), reverse=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super(RoundDetail, self).get_context_data(**kwargs)
        context['league'] = League.objects.get(
            name__icontains=self.kwargs['league_name'])
        context['round'] = self.kwargs['round_number']
        return context


class PlayerPositionsView(AdminCheckMixin, FormView):
    template_name = 'add_positions.html'
    form_class = PlayerPositionsFormSet

    def get_context_data(self, **kwargs):
        context = super(PlayerPositionsView, self).get_context_data(**kwargs)
        context['round'] = self.kwargs['round_number']
        context['league'] = League.objects.get(
            name__icontains=self.kwargs['league_name'])
        return context

    def get_success_url(self):
        kwargs = self.kwargs
        kwargs['round_number'] = 1
        kwargs['rule_number'] = 1
        return reverse('add_points', kwargs=kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        round = Round.objects.get(
            league__name__icontains=self.kwargs['league_name'],
            number=self.kwargs['round_number']
        )
        kwargs['round'] = round
        return kwargs

    def form_valid(self, form):
        for subform in form:
            subform.save()
        return super(PlayerPositionsView, self).form_valid(form)


class PlayerPointsView(AdminCheckMixin, TemplateView):
    template_name = 'add_points.html'
    success_url = '/success/'
    model = PlayerPoints
    formset_class = PlayerPointsFormSet
    form_class = PlayerPointsForm

    def get_context_data(self, **kwargs):
        context = super(PlayerPointsView, self).get_context_data(**kwargs)
        league = League.objects.get(name__icontains=self.kwargs['league_name'])
        context['league'] = league
        context['rule'] = LeagueRule.objects.get(
            number=self.kwargs['rule_number'],
            league=league
        )
        context['players'] = Player.objects.filter(league=league)
        context['form'] = self.get_form()
        return context

    def get_form(self):
        league = League.objects.get(name__icontains=self.kwargs['league_name'])
        rule = LeagueRule.objects.get(league=league,
                                      number=self.kwargs['rule_number'])
        round = Round.objects.get(league=league,
                                  number=self.kwargs['round_number'])
        initial = {
            'round': round,
            'rule': rule,
            'points': 0
        }
        kwargs = self.get_form_kwargs()
        if self.request.method == "POST":
            formset = self.get_formset_class(extra=1)(data=self.request.POST,
                                                      rule=rule,
                                                      form_kwargs=kwargs,
                                                      empty_initial=initial)
        else:
            formset = self.get_formset_class(
                extra=1)(rule=rule, form_kwargs=kwargs, empty_initial=initial)
            for form in formset:
                if not form.instance.id:
                    form.initial = initial
        return formset

    def get_form_kwargs(self):
        league = League.objects.get(name__icontains=self.kwargs['league_name'])
        round = Round.objects.filter(number=self.kwargs['round_number'],
                                     league=league)
        rule = LeagueRule.objects.get(league=league,
                                      number=self.kwargs['rule_number'])
        kwargs = {'rule': rule, 'league': league, 'round': round}
        return kwargs

    def get_formset_class(self, extra=1):
        return modelformset_factory(
            self.model,
            fields=['player', 'round', 'rule', 'points'],
            formset=self.formset_class,
            form=self.form_class,
            extra=extra
        )

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            for subform in form:
                if subform.is_valid():
                    subform.save()
        messages.success(self.request,
                         "Scores successfully updated!")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        league_name = self.kwargs['league_name']
        round_number = self.kwargs['round_number']
        current_rule_number = self.kwargs['rule_number']

        next_rule = LeagueRule.objects.filter(
            league__name=league_name,
            number__gt=current_rule_number
        ).order_by('id').first()

        if next_rule:
            return reverse(
                'add_points',
                kwargs={
                    'league_name': league_name,
                    'round_id': round_number,
                    'rule_id': next_rule.id
                }
            )
        return reverse(
            'round_detail',
            kwargs={'league_name': league_name, 'round_number': round_number}
        )

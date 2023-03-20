from django.views.generic import TemplateView, FormView, ListView
from django.urls import reverse

from .forms import  PlayerPointsFormSet
from .models import Player, Round, LeagueRule


class LeagueHome(ListView):
    template_name = 'league_home.html'
    model = Player

    def get_queryset(self):
        return sorted(Player.objects.filter(
            league__name=self.kwargs['league_name']
        ), key= lambda a: a.points)


class Rounds(ListView):
    template_name = 'rounds.html'
    model = Round

    def get_queryset(self):
        return Round.objects.filter(league_name=self.kwargs['league_name'])


class RoundDetail(ListView):
    template_name = 'round_detail.html'
    model = Player

    def get_queryset(self):
        pass


class PlayerPointsView(FormView):
    template_name = 'add_points.html'
    success_url = '/success/'

    def get_context_data(self, *args, **kwargs):
        context = super(PlayerPointsView, self).get_context_data(*args, **kwargs)
        import pdb; pdb.set_trace()
        context['rule'] = LeagueRule.objects.get(
            number=self.kwargs['rule_number'],
            league__name__icontains=self.kwargs['league_name']
        )
        return context

    def get_form_kwargs(self):
        kwargs = super(PlayerPointsView, self).get_form_kwargs()
        kwargs.update({
            'league': self.kwargs['league_name'],
            'rule': self.kwargs['rule_number'],
            'round': self.kwargs['round_number']
        })
        return kwargs

    def get_form(self):
        kwargs = self.get_form_kwargs()
        return PlayerPointsFormSet(form_kwargs=kwargs)

    def form_valid(self, form):
        for subform in form:
            subform.save()
        return super().form_valid(form)

    def get_success_url(self):
        league_name = self.kwargs['league_name']
        round_number = self.kwargs['round_number']
        current_rule_number = self.kwargs['rule_number']

        next_rule = LeagueRule.objects.filter(
            league__name=league_name,
            round_number=round_number,
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
            'round-detail',
            kwargs={'league_id': league_name, 'round_id': round_number}
        )


class AddPositionsView(FormView):
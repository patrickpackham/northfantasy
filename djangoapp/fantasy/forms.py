from django.forms import formset_factory, ModelForm, ValidationError, \
    ModelChoiceField, IntegerField
from .models import PlayerPoints, Round, Player, LeagueRule, League,\
    PlayerRoundPosition


class PlayerPositionForm(ModelForm):
    class Meta:
        model = PlayerRoundPosition
        fields = ['round', 'player', 'position']


class PlayerPointsForm(ModelForm):
    class Meta:
        model = PlayerPoints
        fields = ['player', 'round', 'rule', 'points']

    def __init__(self, *args, **kwargs):
        league = League.objects.get(name__icontains=kwargs.pop('league'))
        round = kwargs.pop('round')
        rule = kwargs.pop('rule')
        super(PlayerPointsForm, self).__init__(*args, **kwargs)
        self.fields['round'].queryset = Round.objects.filter(
            league=league, number=round)
        self.fields['rule'].label = LeagueRule.objects.get(
            league=league, number=rule).title
        self.fields['player'].queryset = Player.objects.filter(league=league)
        self.fields['points'] = IntegerField()

    def clean(self):
        cleaned_data = super().clean()
        round = cleaned_data.get('round')
        player = cleaned_data.get('player')
        position = cleaned_data.get('position')
        rule = cleaned_data.get('rule')
        if round and player and position and rule:
            if position == "Midfield":
                cleaned_data['points'] = rule.midfield_points
            elif position == "Forward":
                cleaned_data['points'] = rule.forward_points
            elif position == "Defender":
                cleaned_data['points'] = rule.defender_points
            elif position == "Keeper":
                cleaned_data['points'] = rule.keeper_points
            else:
                raise ValidationError("Invalid position")


PlayerPointsFormSet = formset_factory(PlayerPointsForm, extra=2)
PlayerPositinoFormSet = formset_factory(PlayerPositionForm)

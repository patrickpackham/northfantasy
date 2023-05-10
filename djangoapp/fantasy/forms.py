from django.forms import (
    modelformset_factory,
    formset_factory,
    ModelForm,
    Form,
    ValidationError,
    MultipleChoiceField,
    IntegerField,
    HiddenInput,
    BaseModelFormSet,
    TextInput,
    CheckboxSelectMultiple,
)
from .models import PlayerPoints, Player, PlayerRoundPosition


class PlayerPositionForm(ModelForm):
    class Meta:
        model = PlayerRoundPosition
        fields = ["round", "player", "position", "id"]
        widgets = {"round": HiddenInput()}


class BasePlayerPositionFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        round = kwargs.pop("round")
        players = Player.objects.filter(league=round.league)
        for player in players:
            PlayerRoundPosition.objects.get_or_create(
                defaults={"position": player.default_position},
                player=player,
                round=round,
            )
        super(BasePlayerPositionFormSet, self).__init__(*args, **kwargs)
        self.queryset = PlayerRoundPosition.objects.filter(
            player__in=players, round=round
        )
        for form in self.forms:
            form.fields["player"].widget.attrs.update({"class": "form-control"})
            form.fields["position"].widget.attrs.update({"class": "form-control"})


class PlayerPointsForm(ModelForm):
    class Meta:
        model = PlayerPoints
        fields = ["id", "player", "round", "rule", "points"]
        widgets = {
            "round": HiddenInput(),
            "rule": HiddenInput(),
            "points": HiddenInput(),
            "id": HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        league = kwargs.pop("league")
        round = kwargs.pop("round")
        rule = kwargs.pop("rule")
        players = Player.objects.filter(league=league)
        super(PlayerPointsForm, self).__init__(*args, **kwargs)
        self.fields["rule"].label = rule.title
        self.fields["round"].queryset = round
        self.fields["player"].queryset = players
        self.fields["player"].label = ""


class BasePlayerPointsFormSet(BaseModelFormSet):
    empty_initial = {}

    def __init__(self, *args, **kwargs):
        rule = kwargs.pop("rule")
        self.empty_initial = kwargs.pop("empty_initial")
        super(BasePlayerPointsFormSet, self).__init__(*args, **kwargs)
        self.queryset = PlayerPoints.objects.filter(rule=rule)
        for form in self.forms:
            form.fields["player"].widget.attrs.update({"class": "form-control mt-3"})
            form.empty_permitted = True

    @property
    def empty_form(self):
        empty_form = super(BasePlayerPointsFormSet, self).empty_form
        empty_form.initial = self.empty_initial
        empty_form.fields["player"].widget.attrs.update({"class": "form-control mt-3"})
        return empty_form


PlayerPositionsFormSet = modelformset_factory(
    PlayerRoundPosition,
    fields=["round", "player", "position", "id"],
    formset=BasePlayerPositionFormSet,
    form=PlayerPositionForm,
    extra=0,
)

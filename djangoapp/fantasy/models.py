from django.db import models

POSITION_CHOICES = [("Keeper", "Keeper"),
                    ("Defender", "Defender"),
                    ("Midfield", "Midfield"),
                    ("Forward", "Forward")]


class League(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Player(models.Model):
    name = models.CharField(max_length=255)
    league = models.ForeignKey('League', on_delete=models.CASCADE, unique=True)

    @property
    def points(self):
        points = self.playerpoints_set.all()
        return points.aggregate(models.Sum('points'))['points__sum']

    @property
    def goals(self):
        goal_points = self.playerpoints_set.filter(
            rule__title__icontains='goals')
        return goal_points.count()

    @property
    def assists(self):
        assist_points = self.playerpoints_set.filter(
            rule__title__icontains='assist'
        )
        return assist_points.count()


class Round(models.Model):
    number = models.IntegerField()
    league = models.ForeignKey('League', on_delete=models.CASCADE)


class LeagueRule(models.Model):
    title = models.CharField(max_length=1024)
    number = models.IntegerField()
    league = models.ForeignKey('League', on_delete=models.CASCADE)
    midfield_points = models.IntegerField()
    forward_points = models.IntegerField()
    defender_points = models.IntegerField()
    keeper_points = models.IntegerField()

    def __str__(self):
        return self.title


class PlayerPoints(models.Model):
    rule = models.ForeignKey('LeagueRule', on_delete=models.CASCADE)
    player_position = models.CharField(max_length=64, choices=POSITION_CHOICES)
    points = models.IntegerField()


class PlayerRoundPosition(models.Model):
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    round = models.ForeignKey('Round', on_deete=models.CASCADE)
    position = models.ChoiceField(choices=POSITION_CHOICES)
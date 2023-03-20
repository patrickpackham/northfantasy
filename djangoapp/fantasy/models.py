from django.db import models

POSITION_CHOICES = [("Keeper", "Keeper"),
                    ("Defender", "Defender"),
                    ("Midfield", "Midfield"),
                    ("Forward", "Forward")]


class League(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=255)
    league = models.ForeignKey('League', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def points(self, round=None):
        points = self.playerpoints_set.all()
        if round:
            points = points.filter(round=round)
        points = points.aggregate(models.Sum('points'))['points__sum']
        return points if points else 0

    def goals(self, round=None):
        goal_points = self.playerpoints_set.filter(
            rule__title__icontains='goals')
        if round:
            goal_points = goal_points.filter(round=round)
        return goal_points.count()

    def assists(self, round=None):
        assist_points = self.playerpoints_set.filter(
            rule__title__icontains='assist')
        if round:
            assist_points = assist_points.filter(round=round)
        return assist_points.count()


class Round(models.Model):
    number = models.IntegerField()
    league = models.ForeignKey('League', on_delete=models.CASCADE)
    played = models.BooleanField(default=False)


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
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    round = models.ForeignKey('Round', on_delete=models.CASCADE)
    points = models.IntegerField()

    class Meta:
        verbose_name_plural = "Player points"


class PlayerRoundPosition(models.Model):
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    round = models.ForeignKey('Round', on_delete=models.CASCADE)
    position = models.CharField(max_length=256, choices=POSITION_CHOICES)
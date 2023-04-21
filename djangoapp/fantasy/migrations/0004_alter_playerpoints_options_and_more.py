# Generated by Django 4.1 on 2023-03-20 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("fantasy", "0003_leaguerule_number_alter_league_name_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="playerpoints",
            options={"verbose_name_plural": "Player points"},
        ),
        migrations.RemoveField(
            model_name="playerpoints",
            name="player",
        ),
        migrations.RemoveField(
            model_name="playerpoints",
            name="position",
        ),
        migrations.RemoveField(
            model_name="playerpoints",
            name="round",
        ),
        migrations.AddField(
            model_name="playerpoints",
            name="player_position",
            field=models.CharField(
                choices=[
                    ("Keeper", "Keeper"),
                    ("Defender", "Defender"),
                    ("Midfield", "Midfield"),
                    ("Forward", "Forward"),
                ],
                default="Midfield",
                max_length=64,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="player",
            name="league",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="fantasy.league"
            ),
        ),
        migrations.CreateModel(
            name="PlayerRoundPosition",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "position",
                    models.CharField(
                        choices=[
                            ("Keeper", "Keeper"),
                            ("Defender", "Defender"),
                            ("Midfield", "Midfield"),
                            ("Forward", "Forward"),
                        ],
                        max_length=256,
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="fantasy.player"
                    ),
                ),
                (
                    "round",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="fantasy.round"
                    ),
                ),
            ],
        ),
    ]

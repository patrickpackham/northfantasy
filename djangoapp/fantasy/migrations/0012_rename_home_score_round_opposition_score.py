# Generated by Django 4.1 on 2023-05-10 06:07

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("fantasy", "0011_round_home_score_round_our_score"),
    ]

    operations = [
        migrations.RenameField(
            model_name="round",
            old_name="home_score",
            new_name="opposition_score",
        ),
    ]

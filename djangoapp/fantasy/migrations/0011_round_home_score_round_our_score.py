# Generated by Django 4.1 on 2023-05-10 06:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fantasy", "0010_alter_playerpoints_rule"),
    ]

    operations = [
        migrations.AddField(
            model_name="round",
            name="home_score",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="round",
            name="our_score",
            field=models.IntegerField(default=0),
        ),
    ]
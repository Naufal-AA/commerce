# Generated by Django 3.0.8 on 2020-08-14 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0025_auto_20200813_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='watched',
            field=models.BooleanField(default='False'),
        ),
    ]

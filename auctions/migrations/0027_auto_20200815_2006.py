# Generated by Django 3.0.8 on 2020-08-15 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0026_watchlist_watched'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='list',
            name='currentbid',
            field=models.CharField(default='No Bid', max_length=10),
        ),
        migrations.AlterField(
            model_name='list',
            name='finalbid',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='list',
            name='startbid',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]

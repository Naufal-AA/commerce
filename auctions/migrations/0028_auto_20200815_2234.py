# Generated by Django 3.0.8 on 2020-08-15 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0027_auto_20200815_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='currentbid',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]

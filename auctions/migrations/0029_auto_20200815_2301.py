# Generated by Django 3.0.8 on 2020-08-15 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0028_auto_20200815_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='currentbid',
            field=models.CharField(default='No Bid', max_length=10),
        ),
    ]

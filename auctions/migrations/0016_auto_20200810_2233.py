# Generated by Django 3.0.8 on 2020-08-10 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_auto_20200810_1014'),
    ]

    operations = [
        migrations.RenameField(
            model_name='list',
            old_name='username',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='list',
            name='finalbid',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='list',
            name='startbid',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]

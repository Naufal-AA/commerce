# Generated by Django 3.0.8 on 2020-07-28 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20200728_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, upload_to='media'),
        ),
    ]
# Generated by Django 3.0.8 on 2020-08-17 22:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0032_auto_20200815_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.RemoveField(
            model_name='bid',
            name='lists',
        ),
        migrations.AddField(
            model_name='bid',
            name='lists',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='list', to='auctions.List'),
            preserve_default=False,
        ),
    ]

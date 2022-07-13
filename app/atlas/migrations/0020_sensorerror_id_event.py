# Generated by Django 4.0.5 on 2022-07-11 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('atlas', '0019_objectevent_operating_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensorerror',
            name='id_event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='error_event', to='atlas.objectevent', verbose_name='Ошибка'),
        ),
    ]
# Generated by Django 4.0.5 on 2022-07-07 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atlas', '0018_remove_objectevent_operating_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='objectevent',
            name='operating_time',
            field=models.FloatField(blank=True, null=True, verbose_name='Наработка, час'),
        ),
    ]

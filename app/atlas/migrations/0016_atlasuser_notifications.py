# Generated by Django 4.0.5 on 2022-07-05 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atlas', '0015_alter_objectevent_id_object_alter_objectevent_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='atlasuser',
            name='notifications',
            field=models.BooleanField(blank=True, default=False, verbose_name='Уведомления'),
        ),
    ]
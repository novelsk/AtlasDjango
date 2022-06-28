# Generated by Django 4.0.5 on 2022-06-28 06:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('atlas', '0008_alter_sensordata_id_error_log_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensormlsettings',
            name='id_sensor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_sensor', to='atlas.sensor', verbose_name='Датчик'),
        ),
        migrations.AlterField(
            model_name='sensormlsettings',
            name='info',
            field=models.CharField(max_length=100, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='sensormlsettings',
            name='point',
            field=models.IntegerField(null=True, verbose_name='Точка'),
        ),
        migrations.AlterField(
            model_name='sensormlsettings',
            name='setting_h',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='sensormlsettings',
            name='setting_hh',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='sensormlsettings',
            name='setting_l',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='sensormlsettings',
            name='setting_ll',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='sensormlsettings',
            name='setting_param_1',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='sensormlsettings',
            name='setting_param_2',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='sensormlsettings',
            name='setting_param_3',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='sensormlsettings',
            name='setting_param_4',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='sensormlsettings',
            name='tm_prd',
            field=models.IntegerField(null=True, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='useraccessgroups',
            name='companys',
            field=models.ManyToManyField(to='atlas.company'),
        ),
        migrations.AlterField(
            model_name='useraccessgroups',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]

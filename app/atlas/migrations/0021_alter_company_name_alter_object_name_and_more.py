# Generated by Django 4.0.5 on 2022-07-11 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atlas', '0020_sensorerror_id_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='object',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Название'),
        ),
    ]
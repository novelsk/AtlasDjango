# Generated by Django 4.0.4 on 2022-06-08 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atlas', '0004_alter_ai_datacheck_alter_ai_dataout'),
    ]

    operations = [
        migrations.AddField(
            model_name='atlasuser',
            name='division',
            field=models.CharField(default=str, max_length=50, verbose_name='Подразделение'),
        ),
        migrations.AddField(
            model_name='atlasuser',
            name='middle_name',
            field=models.CharField(default=str, max_length=50, verbose_name='Отчество'),
        ),
        migrations.AddField(
            model_name='atlasuser',
            name='organization',
            field=models.CharField(default=str, max_length=50, verbose_name='Организация'),
        ),
        migrations.AddField(
            model_name='atlasuser',
            name='post',
            field=models.CharField(default=str, max_length=50, verbose_name='Должность'),
        ),
    ]

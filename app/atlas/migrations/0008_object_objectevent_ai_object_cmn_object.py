# Generated by Django 4.0.4 on 2022-06-14 12:23

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('atlas', '0007_alter_atlasuser_division_alter_atlasuser_middle_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Объект')),
                ('info', models.CharField(max_length=100, verbose_name='Информация')),
            ],
        ),
        migrations.CreateModel(
            name='ObjectEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('p', 'Запланирована'), ('w', 'В работе'), ('c', 'Завершена')], default='p', max_length=1, verbose_name='Статус')),
                ('date_of_creation', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')),
                ('date_of_service_planned', models.DateTimeField(blank=True, default=datetime.datetime(2022, 6, 14, 15, 23, 26, 241670), verbose_name='Запланировано')),
                ('plan', models.CharField(blank=True, max_length=300, verbose_name='План работ')),
                ('date_of_service_completed', models.DateTimeField(blank=True, db_index=True, verbose_name='Выполненно')),
                ('comment', models.CharField(blank=True, max_length=300, verbose_name='Комментарий проведеных работ')),
                ('idobj', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='object', to='atlas.object', verbose_name='Объект')),
            ],
        ),
        migrations.AddField(
            model_name='ai',
            name='object',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ai', to='atlas.object'),
        ),
        migrations.AddField(
            model_name='cmn',
            name='object',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cmn', to='atlas.object'),
        ),
    ]

# Generated by Django 4.0.4 on 2022-06-01 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atlas', '0003_alter_atlasuser_objects_ai_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ai',
            name='datacheck',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='ai',
            name='dataout',
            field=models.DateTimeField(null=True),
        ),
    ]

# Generated by Django 4.0.4 on 2022-06-16 17:45

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AtlasUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('middle_name', models.CharField(blank=True, default=str, max_length=50, verbose_name='Отчество')),
                ('organization', models.CharField(blank=True, default=str, max_length=50, verbose_name='Организация')),
                ('division', models.CharField(blank=True, default=str, max_length=50, verbose_name='Подразделение')),
                ('post', models.CharField(blank=True, default=str, max_length=50, verbose_name='Должность')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True, verbose_name='Название')),
                ('info', models.CharField(blank=True, max_length=100, verbose_name='Информация')),
            ],
            options={
                'verbose_name': 'Компания',
                'verbose_name_plural': 'Компании',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Название')),
                ('info', models.CharField(blank=True, max_length=100, verbose_name='Информация')),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='Cхема')),
                ('id_company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='object_company', to='atlas.company', verbose_name='Компания')),
            ],
            options={
                'verbose_name': 'Объект',
                'verbose_name_plural': 'Объекты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='UserAccessGroups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Группа')),
                ('info', models.CharField(blank=True, max_length=100, verbose_name='Информация')),
                ('read', models.BooleanField(default=True, verbose_name='Чтение')),
                ('write', models.BooleanField(default=False, verbose_name='Запись')),
                ('companys', models.ManyToManyField(to='atlas.company')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Группа доступа',
                'verbose_name_plural': 'Группы доступа',
            },
        ),
        migrations.CreateModel(
            name='SensorMLSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.CharField(blank=True, max_length=100, verbose_name='Описание')),
                ('setting_type', models.IntegerField(blank=True, db_index=True, verbose_name='Тип')),
                ('setting_ll', models.FloatField(blank=True)),
                ('setting_l', models.FloatField(blank=True)),
                ('setting_h', models.FloatField(blank=True)),
                ('setting_hh', models.FloatField(blank=True)),
                ('point', models.IntegerField(blank=True, db_index=True, verbose_name='Точка')),
                ('tm_prd', models.IntegerField(blank=True, db_index=True, verbose_name='Тип')),
                ('setting_param_1', models.FloatField(blank=True)),
                ('setting_param_2', models.FloatField(blank=True)),
                ('setting_param_3', models.FloatField(blank=True)),
                ('setting_param_4', models.FloatField(blank=True)),
                ('id_sensor', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='event_sensor', to='atlas.object', verbose_name='Датчик')),
            ],
            options={
                'verbose_name': 'Настройка ML',
                'verbose_name_plural': 'Настройки ML',
            },
        ),
        migrations.CreateModel(
            name='SensorError',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('error', models.IntegerField(blank=True, db_index=True)),
                ('error_start_date', models.DateTimeField(blank=True, verbose_name='Дата начала ошибки')),
                ('error_end_date', models.DateTimeField(blank=True, verbose_name='Дата окончания ошибки')),
                ('info', models.CharField(blank=True, max_length=100, verbose_name='Описание')),
                ('id_sensor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='error_sensor', to='atlas.object', verbose_name='Датчик')),
            ],
            options={
                'verbose_name': 'Ошибка',
                'verbose_name_plural': 'Ошибки',
            },
        ),
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, db_index=True, verbose_name='Дата обработки сигнала')),
                ('mode', models.FloatField()),
                ('ai_max', models.FloatField()),
                ('ai_min', models.FloatField()),
                ('ai_mean', models.FloatField()),
                ('stat_min', models.FloatField()),
                ('stat_max', models.FloatField()),
                ('ml_min', models.FloatField()),
                ('ml_max', models.FloatField()),
                ('status', models.IntegerField(blank=True, db_index=True, verbose_name='Статус')),
                ('id_error_log', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='data_error', to='atlas.object', verbose_name='Датчик')),
                ('id_sensor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='data_sensor', to='atlas.object', verbose_name='Датчик')),
            ],
            options={
                'verbose_name': 'Данные',
                'verbose_name_plural': 'Показатели датчиков',
            },
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Название')),
                ('info', models.CharField(blank=True, max_length=100, verbose_name='Информация')),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='Cхема')),
                ('id_object', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sensor_object', to='atlas.object', verbose_name='Объект')),
            ],
            options={
                'verbose_name': 'Датчик',
                'verbose_name_plural': 'Датчики',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ObjectEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('p', 'Запланирована'), ('w', 'В работе'), ('c', 'Завершена')], default='p', max_length=1, verbose_name='Статус')),
                ('date_of_creation', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')),
                ('date_of_service_planned', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Запланировано')),
                ('plan', models.CharField(blank=True, max_length=300, verbose_name='План работ')),
                ('date_of_service_completed', models.DateTimeField(blank=True, db_index=True, verbose_name='Выполненно')),
                ('comment', models.CharField(blank=True, max_length=300, verbose_name='Комментарий проведеных работ')),
                ('id_object', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='event_object', to='atlas.object', verbose_name='Датчик')),
            ],
            options={
                'verbose_name': 'Операция',
                'verbose_name_plural': 'Операции',
            },
        ),
    ]

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class Company(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название', unique=True)
    info = models.CharField(blank=True, max_length=100, verbose_name='Информация')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        ordering = ['name']


class Object(models.Model):
    id_company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='object_company', verbose_name='Компания')
    name = models.CharField(max_length=40, verbose_name='Название')
    info = models.CharField(blank=True, max_length=100, verbose_name='Информация')
    image = models.ImageField(blank=True, verbose_name='Cхема')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'
        ordering = ['name']


class Sensor(models.Model):
    id_object = models.ForeignKey(Object, on_delete=models.PROTECT, related_name='sensor_object', verbose_name='Объект')
    name = models.CharField(max_length=40, verbose_name='Название')
    info = models.CharField(blank=True, max_length=100, verbose_name='Информация')
    image = models.ImageField(blank=True, verbose_name='Cхема')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'
        ordering = ['name']


class SensorError(models.Model):
    id_sensor = models.ForeignKey(Object, on_delete=models.PROTECT, related_name='error_sensor', verbose_name='Датчик')
    error = models.IntegerField(blank=True, db_index=True)
    error_start_date = models.DateTimeField(blank=True, verbose_name='Дата начала ошибки')
    error_end_date = models.DateTimeField(blank=True, verbose_name='Дата окончания ошибки')
    info = models.CharField(blank=True, max_length=100, verbose_name='Описание')

    def __str__(self):
        return self.id_sensor.name

    class Meta:
        verbose_name = 'Ошибка'
        verbose_name_plural = 'Ошибки'


class SensorData(models.Model):
    id_sensor = models.ForeignKey(Object, on_delete=models.PROTECT, related_name='data_sensor', verbose_name='Датчик')
    id_error_log = models.ForeignKey(SensorError, on_delete=models.PROTECT, null=True, db_index=True, blank=True,
                                     related_name='data_error', verbose_name='Журнал ошибки')
    date = models.DateTimeField(blank=True, db_index=True, verbose_name='Дата обработки сигнала')
    mode = models.FloatField()
    ai_max = models.FloatField()
    ai_min = models.FloatField()
    ai_mean = models.FloatField()
    stat_min = models.FloatField()
    stat_max = models.FloatField()
    ml_min = models.FloatField()
    ml_max = models.FloatField()
    status = models.IntegerField(blank=True, db_index=True, verbose_name='Статус')

    def __str__(self):
        return self.id_sensor.name

    class Meta:
        verbose_name = 'Данные'
        verbose_name_plural = 'Показатели датчиков'


class SensorMLSettings(models.Model):
    id_sensor = models.ForeignKey(Object, on_delete=models.PROTECT, blank=True,
                                  related_name='event_sensor', verbose_name='Датчик')
    info = models.CharField(blank=True, max_length=100, verbose_name='Описание')
    setting_type = models.IntegerField(blank=True, db_index=True, verbose_name='Тип')
    setting_ll = models.FloatField(blank=True)
    setting_l = models.FloatField(blank=True)
    setting_h = models.FloatField(blank=True)
    setting_hh = models.FloatField(blank=True)
    point = models.IntegerField(blank=True, db_index=True, verbose_name='Точка')
    tm_prd = models.IntegerField(blank=True, db_index=True, verbose_name='Тип')
    setting_param_1 = models.FloatField(blank=True)
    setting_param_2 = models.FloatField(blank=True)
    setting_param_3 = models.FloatField(blank=True)
    setting_param_4 = models.FloatField(blank=True)

    def __str__(self):
        return self.id_sensor.name

    class Meta:
        verbose_name = 'Настройка ML'
        verbose_name_plural = 'Настройки ML'


class ObjectEvent(models.Model):
    class Statuses(models.TextChoices):
        PLAN = 'p', 'Запланирована'
        WORK = 'w', 'В работе'
        COMPLETE = 'c', 'Завершена'

    status_json = {
        'p': 'Запланирован',
        'w': 'В работе',
        'c': 'Завершен',
    }

    id_object = models.ForeignKey(Object, on_delete=models.PROTECT, related_name='event_object', verbose_name='Датчик')
    status = models.CharField(max_length=1, choices=Statuses.choices, default=Statuses.PLAN, verbose_name='Статус')
    date_of_creation = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')
    date_of_service_planned = models.DateTimeField(default=timezone.now, blank=True,
                                                   verbose_name='Запланировано')
    plan = models.CharField(max_length=300, blank=True, verbose_name='План работ')
    date_of_service_completed = models.DateTimeField(blank=True, db_index=True, verbose_name='Выполненно')
    comment = models.CharField(max_length=300, blank=True, verbose_name='Комментарий проведеных работ')

    def __str__(self):
        return str(self.id_object) + ' ---- ' + self.status_json[self.status]

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'


class AtlasUser(AbstractUser):
    middle_name = models.CharField(max_length=50, default=str, verbose_name='Отчество', blank=True)
    organization = models.CharField(max_length=50, default=str, verbose_name='Организация', blank=True)
    division = models.CharField(max_length=50, default=str, verbose_name='Подразделение', blank=True)
    post = models.CharField(max_length=50, default=str, verbose_name='Должность', blank=True)

    class Meta(AbstractUser.Meta):
        pass


class UserAccessGroups(models.Model):
    name = models.CharField(max_length=40, verbose_name='Группа')
    info = models.CharField(blank=True, max_length=100, verbose_name='Информация')
    read = models.BooleanField(default=True, verbose_name='Чтение')
    write = models.BooleanField(default=False, verbose_name='Запись')
    companys = models.ManyToManyField(Company)
    users = models.ManyToManyField(AtlasUser)

    def __str__(self):
        rights = ' -'
        if self.read:
            rights += 'r'
        if self.write:
            rights += 'w'
        return str(self.name) + rights

    class Meta:
        verbose_name = 'Группа доступа'
        verbose_name_plural = 'Группы доступа'

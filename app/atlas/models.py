from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from .signals import SensorDataSignals


class Company(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название', unique=True)
    info = models.CharField(blank=True, max_length=100, verbose_name='Информация')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        ordering = ['name']


class Object(models.Model):
    id_company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='object_company',
                                   verbose_name='Компания')
    name = models.CharField(max_length=50, verbose_name='Название')
    info = models.CharField(blank=True, max_length=100, verbose_name='Информация')
    image = models.ImageField(blank=True, verbose_name='Cхема')

    def count_event_not_done(self):
        count = 0
        for event in self.event_object.all():
            if event.not_done():
                count += 1
        return count

    def count_sensors_alerts(self):
        count = 0
        for sensor in self.sensor_object.all():
            count += sensor.error_sensor.filter(confirmed=False).count()
        return count

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'
        ordering = ['name']


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

    id_object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='event_object', verbose_name='Датчик')
    status = models.CharField(max_length=1, choices=Statuses.choices, default=Statuses.PLAN, verbose_name='Статус')
    date_of_creation = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')
    date_of_service_planned = models.DateTimeField(default=timezone.now, blank=True,
                                                   verbose_name='Запланировано')
    operating_time = models.FloatField(null=True, blank=True, verbose_name='Наработка, час')
    plan = models.CharField(max_length=300, blank=False, verbose_name='План работ')
    date_of_service_completed = models.DateTimeField(null=True, blank=True, db_index=True, verbose_name='Выполненно')
    comment = models.CharField(max_length=300, blank=True, verbose_name='Комментарий проведеных работ')

    def not_done(self):
        if timezone.now() > self.date_of_service_planned and self.status != 'c':
            return True
        return False

    def __str__(self):
        return self.status_json[self.status] + ' ' + self.date_of_service_planned.time().__str__()

    class Meta:
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'


class Sensor(models.Model):
    id_object = models.ForeignKey(Object, on_delete=models.PROTECT, related_name='sensor_object', verbose_name='Объект')
    id_sensor_repr = models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Номер датчика в объекте')
    name = models.CharField(max_length=50, verbose_name='Название')
    info = models.CharField(blank=True, max_length=100, verbose_name='Информация')
    image = models.ImageField(blank=True, verbose_name='Cхема')

    def count_alerts(self):
        return self.error_sensor.filter(confirmed=False).count()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'
        ordering = ['name']


class SensorError(models.Model):
    id_sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='error_sensor', verbose_name='Датчик')
    id_event = models.ForeignKey(ObjectEvent, on_delete=models.PROTECT, related_name='error_event',
                                 null=True, blank=True, verbose_name='Ошибка')
    error = models.IntegerField(blank=True, db_index=True)
    error_start_date = models.DateTimeField(blank=True, verbose_name='Дата начала ошибки')
    error_end_date = models.DateTimeField(null=True, verbose_name='Дата окончания ошибки')
    info = models.CharField(null=True, max_length=100, verbose_name='Описание')
    confirmed = models.BooleanField(default=False, verbose_name='Подтвержденная')

    def __str__(self):
        return self.id_sensor.name

    class Meta:
        verbose_name = 'Ошибка'
        verbose_name_plural = 'Ошибки'


class SensorData(models.Model):
    id_sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='data_sensor', verbose_name='Датчик')
    id_error_log = models.ForeignKey(SensorError, on_delete=models.SET_NULL, null=True, db_index=True, blank=True,
                                     related_name='data_error', verbose_name='Журнал ошибки')
    date = models.DateTimeField(blank=True, db_index=True, verbose_name='Дата обработки сигнала')
    mode = models.FloatField(null=True)
    ai_max = models.FloatField(null=True)
    ai_min = models.FloatField(null=True)
    ai_mean = models.FloatField(null=True)
    stat_min = models.FloatField(null=True)
    stat_max = models.FloatField(null=True)
    ml_min = models.FloatField(null=True)
    ml_max = models.FloatField(null=True)
    setting_ll = models.FloatField(null=True)
    setting_l = models.FloatField(null=True)
    setting_h = models.FloatField(null=True)
    setting_hh = models.FloatField(null=True)
    status = models.IntegerField(blank=True, db_index=True, verbose_name='Статус')

    def __str__(self):
        return self.id_sensor.name

    class Meta:
        verbose_name = 'Данные'
        verbose_name_plural = 'Показатели датчиков'


class SensorMLSettings(models.Model):
    id_sensor = models.ForeignKey(Sensor, on_delete=models.SET_NULL, null=True,
                                  related_name='event_sensor', verbose_name='Датчик')
    info = models.CharField(null=True, max_length=100, verbose_name='Описание')
    setting_type = models.IntegerField(null=True, blank=True, db_index=True, verbose_name='Тип')
    setting_ll = models.FloatField(null=True)
    setting_l = models.FloatField(null=True)
    setting_h = models.FloatField(null=True)
    setting_hh = models.FloatField(null=True)
    point = models.IntegerField(null=True, verbose_name='Точка')
    tm_prd = models.IntegerField(null=True, verbose_name='Тип')
    setting_param_1 = models.FloatField(null=True)
    setting_param_2 = models.FloatField(null=True)
    setting_param_3 = models.FloatField(null=True)
    setting_param_4 = models.FloatField(null=True)

    def __str__(self):
        return self.id_sensor.name

    class Meta:
        verbose_name = 'Настройка ML'
        verbose_name_plural = 'Настройки ML'


class AtlasUser(AbstractUser):
    middle_name = models.CharField(max_length=50, verbose_name='Отчество', null=True, blank=True)
    organization = models.CharField(max_length=50, verbose_name='Организация', null=True, blank=True)
    division = models.CharField(max_length=50, verbose_name='Подразделение', null=True, blank=True)
    post = models.CharField(max_length=50, verbose_name='Должность', null=True, blank=True)
    notifications = models.BooleanField(verbose_name='Уведомления', default=False, blank=True)

    def initials(self):
        return self.first_name[:1] + self.last_name[:1]

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


# signals
# Избежать ошибку self: создать объект класс сигнала и вызвать метод объекта а не класса
sensor_data_signal = SensorDataSignals
post_save.connect(sensor_data_signal.time_warning, sender=SensorData)

import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres import fields


class Object(models.Model):
    name = models.CharField(max_length=40, verbose_name='Объект')
    info = models.CharField(max_length=100, verbose_name='Информация')
    image = models.ImageField(blank=True, verbose_name='Cхема')


class Cmn(models.Model):
    object = models.ForeignKey(Object, on_delete=models.PROTECT, related_name='cmn', null=True)
    idobj = models.IntegerField()
    amount = models.IntegerField()
    data = models.DateTimeField()
    mode = models.FloatField()
    ai1 = models.FloatField()
    ai2 = models.FloatField()
    ai3 = models.FloatField()
    ai4 = models.FloatField()
    ai5 = models.FloatField()
    ai6 = models.FloatField()
    ai7 = models.FloatField()
    ai8 = models.FloatField()
    ai9 = models.FloatField()
    ai10 = models.FloatField()
    access_group = models.IntegerField(verbose_name='Группа доступа')


class Ai(models.Model):
    object = models.ForeignKey(Object, on_delete=models.PROTECT, related_name='ai', null=True)
    idobj = models.IntegerField()
    idai = models.IntegerField()
    datain = models.DateTimeField()
    mode = models.FloatField()
    aimax = models.FloatField()
    aimean = models.FloatField()
    aimin = models.FloatField()
    statmin = models.FloatField()
    statmax = models.FloatField()
    mlmin = models.FloatField()
    mlmax = models.FloatField()
    err = models.IntegerField()
    sts = models.IntegerField()
    dataout = models.DateTimeField(null=True)
    datacheck = models.DateTimeField(null=True)
    cmnt = models.CharField(max_length=50)
    access_group = models.IntegerField(verbose_name='Группа доступа')


class ObjectEvent(models.Model):
    class Statuses(models.TextChoices):
        PLAN = 'p', 'Запланирована'
        WORK = 'w', 'В работе'
        COMPLETE = 'c', 'Завершена'
        __emplty__ = 'Статус работы'

    idobj = models.ForeignKey(Object, on_delete=models.PROTECT, related_name='object', verbose_name='Объект')
    status = models.CharField(max_length=1, choices=Statuses.choices, default=Statuses.PLAN, verbose_name='Статус')
    date_of_creation = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')
    date_of_service_planned = models.DateTimeField(default=datetime.datetime.now(), blank=True,
                                                   verbose_name='Запланировано')
    plan = models.CharField(max_length=300, blank=True, verbose_name='План работ')
    date_of_service_completed = models.DateTimeField(blank=True, db_index=True, verbose_name='Выполненно')
    comment = models.CharField(max_length=300, blank=True, verbose_name='Комментарий проведеных работ')


class AtlasUser(AbstractUser):
    objects_cmn_groups = fields.ArrayField(base_field=models.IntegerField(null=True),
                                           default=list, verbose_name='Группы доступа Сmn')
    objects_ai_groups = fields.ArrayField(base_field=models.IntegerField(null=True),
                                          default=list, verbose_name='Группы доступа Ai')
    middle_name = models.CharField(max_length=50, default=str, verbose_name='Отчество', blank=True)
    organization = models.CharField(max_length=50, default=str, verbose_name='Организация', blank=True)
    division = models.CharField(max_length=50, default=str, verbose_name='Подразделение', blank=True)
    post = models.CharField(max_length=50, default=str, verbose_name='Должность', blank=True)

    class Meta(AbstractUser.Meta):
        pass

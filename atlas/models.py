from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres import fields


class Cmn(models.Model):
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
    dataout = models.DateTimeField()
    datacheck = models.DateTimeField()
    cmnt = models.CharField(max_length=50)
    access_group = models.IntegerField(verbose_name='Группа доступа')


class AtlasUser(AbstractUser):
    objects_cmn_groups = fields.ArrayField(base_field=models.IntegerField(null=True), default=list, verbose_name='Группы доступа Сmn')
    objects_ai_groups = fields.ArrayField(base_field=models.IntegerField(null=True), default=list, verbose_name='Группы доступа Ai')

    class Meta(AbstractUser.Meta):
        pass

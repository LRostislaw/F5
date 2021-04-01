from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import Signal
from .utilities import send_activation_notification

user_registrated = Signal(providing_args=['instance'])


def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


user_registrated.connect(user_registrated_dispatcher)


class puser(AbstractUser):
    user = models.ForeignKey('Puser', on_delete=models.PROTECT, null=True, blank=True,  default=None)
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошёл активацию?')
    is_doctor = models.BooleanField(default=False, verbose_name='Врач?')
    send_messages = models.BooleanField(default=True, verbose_name='Слать оповещания?')

    class Meta(AbstractUser.Meta):
        pass


class TypeData(models.Model):
    user = models.ForeignKey(puser, on_delete=models.PROTECT, null=False)
    label = models.CharField(max_length=50, default='Артериальное давление', null=False)

    class Meta:
        verbose_name = 'Тип данных'
        verbose_name_plural = 'Типы данных'


class AD(models.Model):
    user = models.ForeignKey(puser, on_delete=models.PROTECT, null=False)
    type = models.ForeignKey(TypeData, on_delete=models.CASCADE, related_name='type', null=True)
    systolic_ad = models.IntegerField("Систолическое давление", null=True)
    diastolic_ad = models.IntegerField("Диастолическое давление", null=True)
    time = models.DateTimeField(null=True)

    class Meta:
        verbose_name = 'Ад'
        verbose_name_plural = 'Ад'
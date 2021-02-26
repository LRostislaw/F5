from django.contrib.auth.models import User
from django.db import models


class TypeData(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    label = models.CharField(max_length=50, default='Артериальное давление', null=False)

    class Meta:
        verbose_name = 'Тип данных'
        verbose_name_plural = 'Типы данных'


class AD(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    type = models.ForeignKey(TypeData, on_delete=models.CASCADE, related_name='type', null=True)
    systolic_ad = models.IntegerField("Систолическое давление", null=True)
    diastolic_ad = models.IntegerField("Диастолическое давление", null=True)
    time = models.DateTimeField(null=True)

    class Meta:
        verbose_name = 'Ад'
        verbose_name_plural = 'Ад'
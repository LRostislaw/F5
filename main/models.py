from django.contrib.auth.models import User
from django.db import models


class AD(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    systolic_ad = models.IntegerField("Систолическое давление", null=True)
    diastolic_ad = models.IntegerField("Диастолическое давление", null=True)
    time = models.DateTimeField(null=True)

    class Meta:
        verbose_name = 'Ад'
        verbose_name_plural = 'Ад'
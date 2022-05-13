from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=256)
    phone_number = models.CharField(max_length = 12)
    address = models.CharField(max_length=256)
    linkman = models.CharField(max_length=5)
    is_hospital = models.BooleanField(default=True)
    last_login = models.DateField(auto_now=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

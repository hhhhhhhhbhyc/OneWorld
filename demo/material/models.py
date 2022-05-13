from django.db import models

from user.models import User
# Create your models here.


class Material(models.Model):
    TYPE_CHOICES = (
        ('口罩','口罩'),
        ('防护服','防护服'),
        ('护目镜','护目镜'),
        ('呼吸机','呼吸机'),
        ('血袋','血袋'),
        ('药品','药品'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mname = models.CharField(max_length=30)
    postscript = models.TextField(max_length=100)
    number = models.PositiveIntegerField()
    is_match = models.BooleanField(default=False)
    match_id = models.IntegerField(default=-1)
    add_date = models.DateField(auto_now=True)
    type = models.CharField(max_length=50,choices=TYPE_CHOICES)
    x1 = models.PositiveIntegerField()
    x2 = models.PositiveIntegerField()
    x3 = models.PositiveIntegerField()

    class Meta:
        verbose_name = '物资'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.mname + '*'+ str(self.number)


from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    nickname = models.CharField(max_length=40,default='')
    alram_hour = models.IntegerField(default=12)
    alram_minute = models.IntegerField(default=0)
    alram_ring = models.BooleanField(default=False)
    led_color = models.CharField(max_length=40,default='')
    led_power = models.IntegerField(default=0)
    led_bright = models.IntegerField(default=5)
    def __str__(self):
        return str(self.username)

class emotion(models.Model):
    user_id = models.ForeignKey('User',on_delete=models.CASCADE, default='',related_name='user_id')
    emotion = models.IntegerField(default=0)
    number = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    day = models.IntegerField(default=0)
    file_name = models.TextField(default='')
    image = models.ImageField(upload_to = 'uploads/',blank=True, null=True)
    def __str__(self):
        return str(str(self.month)+'/'+str(self.day))

class calender_emotion(models.Model):
    u_id = models.ForeignKey('User',on_delete=models.CASCADE, default='',related_name='u_id')
    daily_emotion = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    day = models.IntegerField(default=0)
    def __str__(self) -> str:
        return str(str(self.month)+'/'+str(self.day))
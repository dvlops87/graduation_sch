from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    nickname = models.CharField(max_length=40,default='')
    def __str__(self):
        return str(self.username)

class emotion(models.Model):
    user_id = models.ForeignKey('User',on_delete=models.CASCADE, default='',related_name='user_id')
    emotion = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    day = models.IntegerField(default=0)
    image = models.ImageField(upload_to = 'uploads/',blank=True, null=True)
    def __str__(self):
        return str(str(self.month)+'/'+str(self.day))
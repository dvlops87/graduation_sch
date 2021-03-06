from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
def default_dict():
    emotion_dict = {
	    "angry": 0,
	    "disgust": 0,
	    "scared": 0,
	    "happy": 0,
	    "sad": 0,
	    "surprised": 0,
	    "neutral": 0
    }
    return emotion_dict

class User(AbstractUser):
    alram_hour = models.IntegerField(default=12)
    alram_minute = models.IntegerField(default=0)
    alram_ring = models.BooleanField(default=False)
    alram_sound = models.IntegerField(default=0)
    led_color = models.CharField(max_length=40,default='')
    led_power = models.IntegerField(default=0)
    led_bright = models.IntegerField(default=5)
    get_flower = models.ManyToManyField("flower", related_name="flower_list")
    json_data = models.JSONField(default=default_dict)
    user_emotion = models.ImageField(upload_to = 'uploads/',blank=True, null=True)
    diary_stack = models.IntegerField(default=0)
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
    json_data = models.JSONField(default=dict)
    def __str__(self):
        return str(str(self.month)+'/'+str(self.day))

class calender_emotion(models.Model):
    u_id = models.ForeignKey('User',on_delete=models.CASCADE, default='',related_name='u_id')
    daily_emotion = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    day = models.IntegerField(default=0)
    def __str__(self) -> str:
        return str(str(self.month)+'/'+str(self.day))

class flower(models.Model):
    name = models.CharField(default='', max_length=20)
    flower_name = models.CharField(default='', max_length=20)
    mean = models.CharField(default='', max_length=40)
    recommend = models.TextField(default='')
    image_1 = models.ImageField(upload_to = 'flowers/',blank=True, null=True)
    image_5 = models.ImageField(upload_to = 'flowers/',blank=True, null=True)
    image_10 = models.ImageField(upload_to = 'flowers/',blank=True, null=True)
    thumbnail = models.ImageField(upload_to = 'uploads/',blank=True, null=True)
    flower_img = models.ImageField(upload_to = 'uploads/',blank=True, null=True)
    def __str__(self):
        return self.name



# ?????? ???????????? ?????? ????????? ??? ?????? ?????? ?????? ?????? ?????? (????????? ??????) (?????? ??? ????????)
# if len(emotion)%10 == 0
#   emotion_stack(id)

#   emotions = emotion.object.get(user_id = id).order_by(-id)
#   emotions = emotions[:10] ?????? 10??? ????????????
#   sum_emotion = [0 for i in range(7)]
#   for emotion in emotions : # ?????? 10??? ?????? ??? ??? ???
#       for emo in emotion.sum_emotion : # Model??? JSON??????, emo??? key ???
#           sum_emotion[i] = emotion.sum_emotion[emo]['howmany']
#           i += 1
#   print(sum_emotion)
# 
# 
# 
# 
# ??????(1??????) ??????(5??????) ??????(10??????) 3????????? ?????????.

# ????????? ?????? ?????? 10??? ????????? ??????

# ????????? ???????????? ??????
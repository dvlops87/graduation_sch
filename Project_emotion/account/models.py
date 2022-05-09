from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    alram_hour = models.IntegerField(default=12)
    alram_minute = models.IntegerField(default=0)
    alram_ring = models.BooleanField(default=False)
    alram_sound = models.IntegerField(default=0)
    led_color = models.CharField(max_length=40,default='')
    led_power = models.IntegerField(default=0)
    led_bright = models.IntegerField(default=5)
    get_flower = models.ManyToManyField("flower", related_name="flower_list") 
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
    mean = models.CharField(default='', max_length=40)
    recommend = models.TextField(default='')
    image = models.ImageField(upload_to = 'flowers/',blank=True, null=True)
    def __str__(self):
        return self.name



# 모델 만들어서 일기 작성할 때 마다 감정 스택 쌓게 하기 (중립은 제외) (최대 몇 스택??)
# if len(emotion)%10 == 0
#   emotion_stack(id)

#   emotions = emotion.object.get(user_id = id).order_by(-id)
#   emotions = emotions[:10] 최근 10개 가져오기
#   sum_emotion = [0 for i in range(7)]
#   for emotion in emotions : # 최근 10개 일기 중 한 개
#       for emo in emotion.sum_emotion : # Model의 JSON필드, emo는 key 값
#           sum_emotion[i] = emotion.sum_emotion[emo]['howmany']
#           i += 1
#   print(sum_emotion)
# 
# 
# 
# 
# 새싹(1일차) 떡잎(5일차) 개화(10일차) 3단계로 나뉜다.

# 회상은 중립 제외 10번 쌓이면 실행

# 도감에 저장되고 없앰
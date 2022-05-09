from django.contrib import admin
from .models import User,emotion, calender_emotion, flower
# Register your models here.
admin.site.register(User)
admin.site.register(emotion)
admin.site.register(calender_emotion)
admin.site.register(flower)
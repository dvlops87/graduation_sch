import numbers ,json, datetime, csv, subprocess
from tkinter.tix import Tree
from tracemalloc import get_object_traceback
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import User, emotion, calender_emotion, flower
from django.contrib import auth
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import json
from random import *


dt_now = datetime.datetime.now()

# 최근 10개 일기 평가 -> 나무 설정
# def emotion_stack(u_id, count):
#     try:
#         emotions = emotion.objects.get(user_id = u_id).order_by(-id)
#         emotions = emotions[:count] # 최근 일기 count개 가져오기
#         sum_emotion = [0 for i in range(7)]
#         for emotion_one in emotions : # 최근 10개 일기 중 한 개
#             i=0
#             for emo in emotion_one.sum_emotion : # Model의 JSON필드, emo는 key 값
#                 sum_emotion[i] = emotion.sum_emotion[emo]['howmany']
#                 i += 1
#         print("최근 ",count,"개 일기 평가 : ",sum_emotion)
#     except:
#         print("아직 일기가 하나도 없습니다.")

# Create your views here.
def user_login(request):
    if request.method == "POST":
        user_id = request.POST["user_id"]
        user_password = '1'
        user = authenticate(username = user_id, password = user_password)
        
        if user is not  None:
            login(request, user)
            print('로그인 성공')
            return redirect('home')
        else:
            print('로그인 실패')
            return render(request, 'login.html', {'error': '아이디와 비밀번호가 일치하지 않습니다.'})
    else:
        return render(request, 'login.html')

def user_signup(request):
    if request.method == "POST" :
        user = User.objects.create_user(
            username = request.POST["user_id"],
            password = '1',
        )
        user.save()
        return render(request, 'finish_signup.html')
    return render(request, 'signup.html')

def home(request):
    now = datetime.datetime.now()
    now_hour = now.hour
    now_minute = now.minute
    user = request.user
    user = get_object_or_404(User, id=user.id)
    if user.alram_hour == now_hour and user.alram_minute == now_minute:
        user.alram_ring = True
        print('성공')
        user.save()
    else:
        user.alram_ring = False
        user.save()
    # emotion_stack(user.id, 10)
    return render(request, 'home.html',{'dt_now':dt_now, 'user':user, 'flowers':user.user_emotion})

def mypage(request, user_id=id):
    now = datetime.datetime.now()
    now_hour = now.hour
    now_minute = now.minute
    details = get_object_or_404(User, id=user_id)
    if details.alram_hour == now_hour and details.alram_minute == now_minute:
        details.alram_ring = True
        print('성공')
        details.save()
    else:
        details.alram_ring = False
        details.save()
    flowers = details.get_flower.all()
    print(flowers)
    fff = flower.objects.all()
    for f in flowers:
        fff = fff.exclude(id = f.id)
    
    return render(request, 'mypage.html', {'details':details, 'flowers':flowers, 'nothave':fff})


def checkUsername(request):
    try:
        user = User.objects.get(username=request.GET['username'])
    except Exception as e:
        user = None
    result = {
        'result':'success',
        # 'data' : model_to_dict(user)  # console에서 확인
        'data' : "not exist" if user is None else "exist"
    }
    return JsonResponse(result)

def calender(request, user_id=id, t_month=dt_now.month , t_day=dt_now.day):
    now = datetime.datetime.now()
    now_hour = now.hour
    now_minute = now.minute
    details = get_object_or_404(User, id=user_id)
    if details.alram_hour == now_hour and details.alram_minute == now_minute:
        details.alram_ring = True
        print('성공')
        details.save()
    else:
        details.alram_ring = False
        details.save()
    try :
        emotions = emotion.objects.filter(Q(user_id=details.id)& Q(month=t_month) & Q(day=t_day))
    except emotion.DoesNotExist:
        emotions = '없습니다.'
        return render(request, 'calender.html', {'details':details, 'emotions':emotions,'t_month':t_month,'t_day':t_day})
    sum_em = [0 for i in range(7)]
    for em in emotions :
        if em.emotion == 0:
            sum_em[0] += 1
        elif em.emotion == 1:
            sum_em[1] += 1
        elif em.emotion == 2:
            sum_em[2] += 1
        elif em.emotion == 3:
            sum_em[3] += 1
        elif em.emotion == 4:
            sum_em[4] += 1
        elif em.emotion == 5:
            sum_em[5] += 1
        elif em.emotion == 6:
            sum_em[6] += 1

    if sum(sum_em) == 0:
        t_emotion ="아직 없습니다."
    else :
        total_emotion = sum_em.index(max(sum_em))
        if total_emotion == 0:
            t_emotion ="화남"
        elif total_emotion == 1:
            t_emotion ="역겨움"
        elif total_emotion == 2:
            t_emotion ="두려움"
        elif total_emotion == 3:
            t_emotion ="행복함"
        elif total_emotion == 4:
            t_emotion ="슬픔"
        elif total_emotion == 5:
            t_emotion ="놀람"
        elif total_emotion == 6:
            t_emotion ="중립"

    return render(request, 'calender.html', {'details':details, 't_emotion':t_emotion, 'emotions':emotions,'t_day':t_day,'t_month':t_month})

def write_diary(request, t_month, t_day, user_id=id):
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')
    nowTime = now.strftime('%H%M')
    file_name = nowDate+'_'+nowTime
    subprocess.run('python /home/lhw/stt/main.py && python /home/lhw/stt/FaceEmotion_ID/facial_emotion_image.py', shell=True) # 동영상 촬영 프로그램 실행
    details = get_object_or_404(User, id=user_id)
    
    now_hour = now.hour
    now_minute = now.minute
    if details.alram_hour == now_hour and details.alram_minute == now_minute:
        details.alram_ring = True
        print('성공')
        details.save()
    else:
        details.alram_ring = False
        details.save()


    # with open('/home/lhw/stt/FaceEmotion_ID/emotion.json', 'r') as f:
    #     json_data = json.load(f)
    # print("감정 판단 결과: ")
    # print(json.dumps(json_data, indent="\t") )


    #나중에 주소 다시 설정
    emotion_json_data = {}
    with open('/home/lhw/leehw/combine_emotion/combinedemotion.json', 'r') as fr:
        emotion_json_data = json.load(fr)
        max_value = int(emotion_json_data['angry']['howmany'])
        default_emotion = 'angry'
        print("default max : ",max_value, " default : ",default_emotion)

    if details.diary_stack == 15:
        details.diary_stack = 0
    details.diary_stack = details.diary_stack +1

    for i in emotion_json_data:
        details.json_data[i]['howmany'] += emotion_json_data[i]['howmany']
        details.save()
        if max_value < emotion_json_data[i]['howmany']:
            max_value = int(emotion_json_data[i]['howmany'])
            default_emotion = i
    print("최종 감정 분류 : ",default_emotion," 값 :",max_value)

    final_emotion_value = 0
    if default_emotion == "angry":
        final_emotion_value = 1
    elif default_emotion == "disgust":
        final_emotion_value = 2
    elif default_emotion == "scared":
        final_emotion_value = 3
    elif default_emotion == "happy":
        final_emotion_value = 4
    elif default_emotion == "sad":
        final_emotion_value = 5
    elif default_emotion == "surprised":
        final_emotion_value = 6
    else:
        final_emotion_value = 0


    default_emotion = emotion.objects.filter(Q(user_id=details.id)& Q(month=t_month) & Q(day=t_day))
    if len(default_emotion) != 0:
        emotions = emotion.objects.create(user_id=details, month=t_month, day=t_day, emotion=final_emotion_value, number=default_emotion[len(default_emotion)-1].number+1,file_name=file_name, json_data=emotion_json_data)
    else:
        emotions = emotion.objects.create(user_id=details, month=t_month, day=t_day, emotion=final_emotion_value, file_name=file_name, json_data=emotion_json_data)
    emotions.save()
    new_emotions = emotion.objects.filter(Q(user_id=details.id)& Q(month=t_month) & Q(day=t_day))
    
    sum_em = [0 for i in range(7)]
    for em in new_emotions :
        if em.emotion == 0:
            sum_em[0] += 1
        elif em.emotion == 1:
            sum_em[1] += 1
        elif em.emotion == 2:
            sum_em[2] += 1
        elif em.emotion == 3:
            sum_em[3] += 1
        elif em.emotion == 4:
            sum_em[4] += 1
        elif em.emotion == 5:
            sum_em[5] += 1
        elif em.emotion == 6:
            sum_em[6] += 1
            
    if sum(sum_em) == 0:
        total_emotion = 0
    else :
        total_emotion = sum_em.index(max(sum_em))
    try :
        c_e = calender_emotion.objects.get(u_id=details, month=t_month, day=t_day)
        c_e.daily_emotion = total_emotion
        c_e.save()
    except calender_emotion.DoesNotExist:
        calender_emotion.objects.create(u_id=details, month=t_month, day=t_day,daily_emotion = total_emotion)
    
    for json in  details.json_data:
        if max_value < json[i]['howmany']:
            max_value = json[i]['howmany']
    
    if details.diary_stack%20 == 10:
        sorted_dict = sorted(details.json_data.items(), key = lambda item: item[1], reverse = True)
        flower_name= next(iter(sorted_dict)) + '_' + str(randint(1,2))
        flower_img= flower.objects.get(name=flower_name) 
        details.user_emotion = flower_img.image_10
        details.save()
    elif details.diary_stack%20 == 1:
        flower_img= flower.objects.get(id=1) 
        details.user_emotion = flower_img.image_1
        details.save()
    elif details.diary_stack%20 == 5:
        flower_img= flower.objects.get(id=1) 
        details.user_emotion = flower_img.image_5
        details.save()
    
    return render(request, 'test.html',{'details':details, 't_day':t_day,'t_month':t_month})



def delete_diary(request, user_id,emotion_id, emotion_num):
    details = get_object_or_404(User, id=user_id)
    now = datetime.datetime.now()
    now_hour = now.hour
    now_minute = now.minute
    if details.alram_hour == now_hour and details.alram_minute == now_minute:
        details.alram_ring = True
        print('성공')
        details.save()
    else:
        details.alram_ring = False
        details.save()

    t_month=dt_now.month
    t_day=dt_now.day
    emotions = get_object_or_404(emotion,user_id=details.id, id=emotion_id, number = emotion_num)
    subprocess.run('rm -rf /media/lhw/flower/work/plus/'+emotions.file_name, shell=True) # 동영상 삭제
    emotions.delete()

    new_emotions = emotion.objects.filter(Q(user_id=details.id)& Q(month=t_month) & Q(day=t_day))
    
    sum_em = [0 for i in range(7)]
    for em in new_emotions :
        if em.emotion == 0:
            sum_em[0] += 1
        elif em.emotion == 1:
            sum_em[1] += 1
        elif em.emotion == 2:
            sum_em[2] += 1
        elif em.emotion == 3:
            sum_em[3] += 1
        elif em.emotion == 4:
            sum_em[4] += 1
        elif em.emotion == 5:
            sum_em[5] += 1
        elif em.emotion == 6:
            sum_em[6] += 1
            
    if sum(sum_em) == 0:
        total_emotion = 0
    else :
        total_emotion = sum_em.index(max(sum_em))

    try :
        c_e = calender_emotion.objects.get(u_id=details, month=t_month, day=t_day)
        c_e.daily_emotion = total_emotion
        c_e.save()
    except calender_emotion.DoesNotExist:
        calender_emotion.objects.create(u_id=details, month=t_month, day=t_day,daily_emotion = total_emotion)

    return render(request, 'test.html',{'details':details, 't_day':t_day,'t_month':t_month})

def view_diary(request, user_id,emotion_id, emotion_num):
    details = get_object_or_404(User, id=user_id)
    now = datetime.datetime.now()
    now_hour = now.hour
    now_minute = now.minute
    if details.alram_hour == now_hour and details.alram_minute == now_minute:
        details.alram_ring = True
        print('성공')
        details.save()
    else:
        details.alram_ring = False
        details.save()

    emotions = get_object_or_404(emotion,user_id=details.id, id=emotion_id, number = emotion_num)
    return render(request, 'diary_detail.html',{'details':details, 'dt_now':dt_now, 'emotions':emotions})

def view_video(user_id,emotion_id, emotion_num):
    details = get_object_or_404(User, id=user_id)
    emotions = get_object_or_404(emotion,user_id=details.id, id=emotion_id, number = emotion_num)
    subprocess.run('xdg-open /media/lhw/flower/work/plus/'+emotions.file_name+'/'+emotions.file_name+'.mp4', shell=True) # 동영상 보기

def view_wordcloud(user_id,emotion_id, emotion_num):
    details = get_object_or_404(User, id=user_id)
    emotions = get_object_or_404(emotion,user_id=details.id, id=emotion_id, number = emotion_num)
    subprocess.run('xdg-open /media/lhw/flower/work/picture/'+emotions.file_name+'/'+emotions.file_name+'.png', shell=True) # 동영상 보기

def set_timer(request, user_id):
    details = get_object_or_404(User, id=user_id)
    now = datetime.datetime.now()
    now_hour = now.hour
    now_minute = now.minute
    if details.alram_hour == now_hour and details.alram_minute == now_minute:
        details.alram_ring = True
        print('성공')
        details.save()
    else:
        details.alram_ring = False
        details.save()

    if request.method == 'POST':
        ampm = request.POST['AMPM']
        hour = int(request.POST['hour'])
        minute = request.POST['minute']
        sound = int(request.POST['alram_sound'])
        if ampm == 'PM':
            hour +=12
        elif hour <10 :
            hour = '0'+str(hour)
        details.alram_hour = hour
        details.alram_minute = minute
        details.alram_sound = int(sound)
        details.save()
        print(hour, minute, sound)
        if float(sound) < 10 :
            sound = '0.0'+str(sound)
        else :
            sound = '0.'+str(sound)
        f = open('/home/lhw/led/sound.txt', 'w') #알람 volume 작성
        f.write(sound)
        f.close()
        f_time = open('/home/lhw/led/time.txt', 'w') #알람 시간 작성
        time = str(hour) +  str(minute)
        f_time.write(time)
        f_time.close()
        return render(request, 'set_timer.html', {'details' : details})
    else :
        return render(request, 'set_timer.html', {'details' : details})


def set_led(request, user_id):
    details = get_object_or_404(User, id=user_id)
    now = datetime.datetime.now()
    now_hour = now.hour
    now_minute = now.minute
    if details.alram_hour == now_hour and details.alram_minute == now_minute:
        details.alram_ring = True
        details.save()
    else:
        details.alram_ring = False
        details.save()

    if request.method == 'POST':
        color = request.POST['color']
        power_radio = int(request.POST['power_radio'])
        led_bright = request.POST.get('led_bright')
        print( details.led_power,power_radio)
        if power_radio == 1:
            details.led_power=1
        elif details.led_power == 1 and power_radio == 0:
            details.led_power = 0
        elif details.led_power == 0 and power_radio == 0:
            details.led_power = 1
        details.led_color = color
        details.led_bright = led_bright
        details.save()
        f_color = open('/home/lhw/led/color.txt', 'w') #led 색상 작성
        f_power = open('/home/lhw/led/onoff.txt', 'w') #led 전원
        f_bright = open('/home/lhw/led/brightness.txt', 'w') #led 밝기
        color = '0x'+color
        f_color.write(color)
        f_power.write(str(power_radio))
        if int(led_bright) < 10:
            led_bright = '0.0'+str(led_bright)
        else :
            led_bright = '0.'+str(led_bright)
        f_bright.write(led_bright)
        f_color.close()
        f_power.close()
        f_bright.close()
        return render(request, 'set_led.html', {'details' : details})
    else :
        return render(request, 'set_led.html', {'details' : details})

@csrf_exempt
def start_led(request):
    jsonObject = json.loads(request.body)
    print('ok')
    subprocess.run('python /home/lhw/led/main_alert.py & python /home/lhw/led/alert_kill.py',shell=True) # LED 알람 실행
    data = {
        "success": '성공',
    }
    return JsonResponse(data)

def flower_detail(request, flower_info):
    flower_detail = flower.objects.get(name = flower_info)
    return render(request, 'flower_detail.html',{'flower_detail':flower_detail})
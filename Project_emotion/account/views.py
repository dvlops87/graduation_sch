import numbers ,json, datetime, csv, subprocess
from tkinter.tix import Tree
from tracemalloc import get_object_traceback
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import User, emotion, calender_emotion
from django.contrib import auth
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt



dt_now = datetime.datetime.now()

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

    return render(request, 'home.html',{'dt_now':dt_now, 'user':user})

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

    if request.method == "POST":
        now_password = request.POST.get("password")
        if check_password(now_password, details.password):
            new_password = request.POST.get("new_password")
            password_check = request.POST.get("password_check")
            if new_password==password_check:
                details.set_password(new_password)
                details.save()
                print('성공')
                return render(request, 'mypage.html', {'details':details})
            else:
                error = '비밀번호가 일치하지 않습니다.'
                return render(request, 'mypage.html', {'details':details, 'error':error})
        else:
            error = '현재 비밀번호가 올바르지 않습니다'
            print('실패')
            return render(request, 'mypage.html', {'details':details,'error':error})
    else:
        return render(request, 'mypage.html', {'details':details})


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
    sum_em = 0
    for em in emotions :
        sum_em += em.emotion
    if sum_em == 0:
        t_emotion ="아직 없습니다."
    else :
        total_emotion = sum_em/len(emotions)
        if total_emotion >= 4:
            t_emotion ="화남"
        elif total_emotion >= 3:
            t_emotion ="지침"
        elif total_emotion >= 2:
            t_emotion ="우울"
        elif total_emotion >= 1:
            t_emotion ="행복"
    return render(request, 'calender.html', {'details':details, 't_emotion':t_emotion, 'emotions':emotions,'t_day':t_day,'t_month':t_month})

def write_diary(request, t_month, t_day, user_id=id):
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')
    nowTime = now.strftime('%H%M')
    file_name = nowDate+'_'+nowTime
    subprocess.run('python /home/choi/test/main.py', shell=True) # 동영상 촬영 프로그램 실행
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


    # f = open('주소 입력', 'r', encoding='utf-8') # 저장된 감정 판단
    f = open('/home/choi/test/z.csv', 'r', encoding='utf-8') # 저장된 감정 판단
    rdr = csv.reader(f)
    emo = []
    for line in rdr:
        emo.append(line[0]) #불러온 데이터 중 감정만 입력, 이건 데이터에 따라 수정해야함
    f.close()

    default_emotion = emotion.objects.filter(Q(user_id=details.id)& Q(month=t_month) & Q(day=t_day))
    if len(default_emotion) != 0:
        emotions = emotion.objects.create(user_id=details, month=t_month, day=t_day, emotion=emo[2], number=default_emotion[len(default_emotion)-1].number+1,file_name=file_name)
    else:
        emotions = emotion.objects.create(user_id=details, month=t_month, day=t_day, emotion=emo[2], file_name=file_name)
    emotions.save()
    new_emotions = emotion.objects.filter(Q(user_id=details.id)& Q(month=t_month) & Q(day=t_day))
    sum_em = 0
    for em in new_emotions :
        sum_em += em.emotion
    if sum_em == 0:
        total_emotion = 0
    else :
        total_emotion = sum_em/len(new_emotions)
    try :
        c_e = calender_emotion.objects.get(u_id=details, month=t_month, day=t_day)
        c_e.daily_emotion = total_emotion
        c_e.save()
    except calender_emotion.DoesNotExist:
        calender_emotion.objects.create(u_id=details, month=t_month, day=t_day,daily_emotion = total_emotion)

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
    subprocess.run('rm -rf /media/choi/flower1/work/plus/'+emotions.file_name, shell=True) # 동영상 삭제
    emotions.delete()

    new_emotions = emotion.objects.filter(Q(user_id=details.id)& Q(month=t_month) & Q(day=t_day))
    sum_em = 0
    for em in new_emotions :
        sum_em += em.emotion
    if sum_em == 0:
        total_emotion = 0
    else :
        total_emotion = sum_em/len(new_emotions)
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
    subprocess.run('mplayer /media/choi/flower1/work/plus/'+emotions.file_name+'/'+emotions.file_name+'.mp4', shell=True) # 동영상 보기
    t_month=dt_now.month
    t_day=dt_now.day
    return render(request, 'test.html',{'details':details, 't_day':t_day,'t_month':t_month})

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
        if ampm == 'PM':
            hour +=12
        elif hour <10 :
            hour = '0'+str(hour)
        details.alram_hour = hour
        details.alram_minute = minute
        print(hour, minute)
        details.save()
        f = open('/home/choi/led/time.txt', 'w') #알람 시간 작성
        time = str(hour) +  str(minute)
        f.write(time)
        f.close()
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
        print('성공')
        details.save()
    else:
        details.alram_ring = False
        details.save()

    if request.method == 'POST':
        color = request.POST['color']
        power_radio = int(request.POST['power_radio'])
        led_bright = int(request.POST.get('led_bright'))
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
        f_color = open('/home/choi/led/color.txt', 'w') #led 색상 작성
        f_power = open('/home/choi/led/onoff.txt', 'w') #led 전원
        f_bright = open('/home/choi/led/brightness.txt', 'w') #led 밝기
        color = '0x'+color
        f_color.write(color)
        f_power.write(str(power_radio))
        f_bright.write(str(led_bright))
        f_color.close()
        f_power.close()
        f_bright.close()
        return render(request, 'set_led.html', {'details' : details})
    else :
        return render(request, 'set_led.html', {'details' : details})

@csrf_exempt
def start_led(request):
    jsonObject = json.loads(request.body)
    subprocess.run(['python /home/choi/led/main_alert.py'],shell=True) # LED 알람 실행
    data = {
        "success": '성공',
    }
    return JsonResponse(data)

from tkinter.tix import Tree
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import User, emotion
from django.contrib import auth
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, JsonResponse
import datetime
import subprocess
import csv



dt_now = datetime.datetime.now()

# Create your views here.
def user_login(request):
    if request.method == "POST":
        user_id = request.POST["user_id"]
        user_password = request.POST["user_password"]
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
            password = request.POST["user_password"],
        )
        user.save()
        return render(request, 'finish_signup.html')
    return render(request, 'signup.html')

def home(request):
    return render(request, 'home.html',{'dt_now':dt_now})

def mypage(request, user_id=id):
    details = get_object_or_404(User, id=user_id)
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
    details = get_object_or_404(User, id=user_id)
    try :
        emotions = emotion.objects.get( user_id=details.id, month=t_month, day=t_day)
    except emotion.DoesNotExist:
        emotions = '없습니다.'
        return render(request, 'calender.html', {'details':details, 'emotions':emotions,'t_month':t_month,'t_day':t_day})
    if emotions.emotion == 1:
        t_emotion ="행복"
    elif emotions.emotion == 2:
        t_emotion ="우울"
    elif emotions.emotion == 3:
        t_emotion ="지침"
    elif emotions.emotion == 4:
        t_emotion ="화남"
    return render(request, 'calender.html', {'details':details, 't_emotion':t_emotion, 'emotions':emotions,'t_day':t_day,'t_month':t_month})

def write_diary(request, t_month, t_day, user_id=id):
    details = get_object_or_404(User, id=user_id)
    f = open('C:\\Users\\tjdgu\\Desktop\\z.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    emo = []
    for line in rdr:
        emo.append(line[0])
        # emo.append(line[1])
    f.close()
    # f = open('C:\Users\tjdgu\Desktop\zz.csv', 'w')
    emotions = emotion.objects.create(user_id=details, month=t_month, day=t_day, emotion=emo[2])
    emotions.save()
    subprocess.run('start C:\\school\\UPF_WCD\\tt.txt', shell=True)
    return render(request, 'test.html',{'details':details, 't_day':t_day,'t_month':t_month})

def delete_diary(request, user_id,emotion_id):
    t_month=dt_now.month
    t_day=dt_now.day
    details = get_object_or_404(User, id=user_id)
    emotions = get_object_or_404(emotion,user_id=details.id, id=emotion_id)
    emotions.delete()
    if emotions.emotion == 1:
        t_emotion ="행복"
    elif emotions.emotion == 2:
        t_emotion ="우울"
    elif emotions.emotion == 3:
        t_emotion ="지침"
    elif emotions.emotion == 4:
        t_emotion ="화남"
    return render(request, 'calender.html', {'details':details, 't_emotion':t_emotion, 'emotions':emotions,'t_day':t_day,'t_month':t_month})

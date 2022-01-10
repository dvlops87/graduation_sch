from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib import auth

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
    return render(request, 'home.html')
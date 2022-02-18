"""emotion_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import account.views as user
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user.user_login, name="login"),
    path('home/', user.home, name="home"),
    path('signup/', user.user_signup, name="signup"),
    path('mypage/<int:user_id>', user.mypage, name="mypage"),
    path('user/api/checkUsername', user.checkUsername),
    path('calender/<int:user_id>/<int:t_month>/<int:t_day>',user.calender, name='calender'),
    path('write_diary/<int:t_month>/<int:t_day>/<int:user_id>', user.write_diary, name="write_diary"),
    path('delete_diary/<int:user_id>/<int:emotion_id>/<int:emotion_num>', user.delete_diary, name="delete_diary"),
    path('view_diary/<int:user_id>/<int:emotion_id>/<int:emotion_num>', user.view_diary, name="view_diary"),
    path('set_timer/<int:user_id>', user.set_timer, name="set_timer"),
    path('set_led/<int:user_id>', user.set_led, name="set_led"),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

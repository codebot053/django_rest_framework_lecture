from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('',views.UserApiView.as_view(),name='user_api_view'), #가입된 유저정보,작성글정보 API 조회
    path('signup/',views.UserSignupApiView.as_view(),name='user_api_view'), #신규 회원가입
    path('login/',views.UserLoginView.as_view(),name='user_login_view'), #유저 로그인
]   
from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('',views.UserApiView.as_view(),name='user_api_view'), #로그인, 가입 api 담당
]
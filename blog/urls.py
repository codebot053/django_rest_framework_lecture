from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('',views.ArticleApiView.as_view(),name='user_api_view'), #유저 가입시간, 현재시간 출력
    
]
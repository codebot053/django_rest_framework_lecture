from django.shortcuts import render
from datetime import datetime,timedelta,date,timezone
import pytz

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import permissions, status

from django.db.models import F, Sum, Count, Case, When
from django.contrib.auth import authenticate, login
from django.conf import settings
# serializer
from user.serializers import UserSerializer, MyArticleSerializer
# user models
from user.models import User, UserProfile, Hobby
# blog models
from blog.models import Article, Category
# # Create your views here. 
# Create your views here.

class ArticleApiView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self,request):
        userinfo = request.data.get('user')
        username = userinfo.get('username', '')
        password = userinfo.get('password', '')
        user_name=request.data["user"]["username"]
        request.data["user"] = User.objects.get(username=user_name).id
        print(request.data)
        user = authenticate(request, username=username, password=password)

        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        # TypeError: can’t compare offset-naive and offset-aware datetimes 
        # https://thewebdev.info/2022/04/04/how-to-fix-typeerror-cant-compare-offset-naive-and-offset-aware-datetimes-with-python/
        # 참조
        current_user_id = request.user.id
        current_user_join_date = request.user.join_date
        # offset-naive to offset-aware 
        # datetime.now() : offset-naive
        # datetime.now(timezone.utc) : offset-aware
        now_date_time = datetime.now(timezone.utc)
        three_minutes_limit = now_date_time - timedelta(minutes=3)
        
        if current_user_join_date <= three_minutes_limit:
            auth_to_write = True
            article_serializer = MyArticleSerializer(data=request.data)
            # print(article_serializer.initial_data)
            # 조건문을 쓰지않고 
            # article_serializer.is_valid(raise_exception=True)
            # 를 사용하면 validate 실패시 .is_valid 를 넘어가지 않고 exception을 띄어준다.
            if article_serializer.is_valid():
                article_serializer.save()
                return Response({'현재 시간': now_date_time,
                        '3분 전' : three_minutes_limit,
                        '유저 가입시간': current_user_join_date,
                        '작성가능':auth_to_write,
                        '작성글':article_serializer.data},status=status.HTTP_201_CREATED)
            else:

                return Response(article_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        auth_to_write = False
        
        return Response({
                        '현재 시간': now_date_time,
                        '3분 전' : three_minutes_limit,
                        '유저 가입시간': current_user_join_date,
                        '작성가능': auth_to_write
        },status=status.HTTP_400_BAD_REQUEST)
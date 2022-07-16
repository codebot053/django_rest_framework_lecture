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
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(request, username=username, password=password)

        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        # TypeError: can’t compare offset-naive and offset-aware datetimes 
        # https://thewebdev.info/2022/04/04/how-to-fix-typeerror-cant-compare-offset-naive-and-offset-aware-datetimes-with-python/
        # 참조
        
        current_user_join_date = request.user.join_date
        now_date_time = datetime.now(timezone.utc)
        three_minutes_limit = now_date_time - timedelta(minutes=3)
        
        if current_user_join_date <= three_minutes_limit:
            auth_to_write = True
            return Response({'현재 시간': now_date_time,
                        '3분 전' : three_minutes_limit,
                        '유저 가입시간': current_user_join_date,
                        '작성가능':auth_to_write},status=status.HTTP_200_OK)
        auth_to_write = False
        return Response({
                        '현재 시간': now_date_time,
                        '3분 전' : three_minutes_limit,
                        '유저 가입시간': current_user_join_date,
                        '작성가능': auth_to_write
        },status=status.HTTP_400_BAD_REQUEST)
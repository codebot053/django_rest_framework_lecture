from xmlrpc.client import ResponseError
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import permissions, status

from django.db.models import F, Sum, Count, Case, When
from django.contrib.auth import authenticate, login
from django.conf import settings
# serializer
from user.serializers import UserSerializer
# user models
from user.models import User, UserProfile, Hobby
# # Create your views here. 

class UserApiView(APIView):
    # 로그인
    permission_classes = [permissions.AllowAny]
    
    def get(self,request):
        # 정참조ex
        '''
        user_profile = UserProfile.objects.get(id=1)
        user_profile.user
        user_profile.hobby
        '''
        # 역참조ex
        '''
        hobby = Hobby.objects.get(id=1)
        hobby.userprofile_set
        '''
        # 모든 사용자에 대해서 user 정보와 userprofile 정보를 가져오고
        # 같은 취미를 가진 사람들을 출력하기
        print("user get input!")

        # UserSerializer() 안에 queryset 이나 object를 넣어주면 된다.
        # 'User.objects.all()' 과 같이 queryset 으로 불러올경우 'many=True'를 뒤에 써야한다.
        # UserSerializer() 뒤에 .data 를 적어야 JSON 형태의 데이터가 불러와진다.
        # 아래 코드는 queryset 일때!
        #return Response(UserSerializer(User.objects.all(), many=True).data, status=status.HTTP_200_OK)
        # 아래 코드는 단일 object 일때! (단일 object 는 'many=True'를 사용하지 않는다.)
        #return Response(UserSerializer(User.objects.all().first()).data, status=status.HTTP_200_OK)
        # 만약 랜덤으로 user를 뽑을 경우에는 아래와 같이 한다.
        return Response(UserSerializer(User.objects.all().order_by('?').first()).data, status=status.HTTP_200_OK)
        #return Response({"message": "get success!!"})

    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(request, username=username, password=password)
        
        
        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return Response({"message": "로그인 성공!!"}, status=status.HTTP_200_OK)
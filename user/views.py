from xmlrpc.client import ResponseError
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import permissions, status

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.db.models import F, Sum, Count, Case, When
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth.hashers import check_password

# serializer
from user.serializers import UserSerializer, MyArticleSerializer
# user models
from user.models import User, UserProfile, Hobby
# blog models
from blog.models import Article, Category
import jwt
from django_drf.settings import SIMPLE_JWT
from django.contrib.auth import get_user
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
import rest_framework_simplejwt
# # Create your views here. 

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    # 로그인
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()

        if user is None: # 해당 email의 user가 존재하지 않는 경우
            return Response(
                {"message": "존재하지않는 user입니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        if not check_password(password, user.password): # 비밀번호에서 틀린 경우
            return Response(
                {"message": "비밀번호가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST
            )
        
        if user is not None: # 모두 성공 시
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            response = Response(
                {
                    "user": UserSerializer(user).data,
                    "message": "login success",
                    "jwt_token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status=status.HTTP_200_OK
            )
            response.set_cookie("access_token", access_token, httponly=True)
            response.set_cookie("refresh_token", refresh_token, httponly=True)
            return response
        else: # 그 외
            return Response(
                {"message": "로그인에 실패하였습니다"}, status=status.HTTP_400_BAD_REQUEST
            )
class UserApiView(APIView):
    # 회원가입
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
        return Response(UserSerializer(User.objects.all(), many=True).data, status=status.HTTP_200_OK)

        # 아래 코드는 단일 object 일때! (단일 object 는 'many=True'를 사용하지 않는다.)
        #return Response(UserSerializer(User.objects.all().first()).data, status=status.HTTP_200_OK)

        # 만약 랜덤으로 user를 뽑을 경우에는 아래와 같이 한다.
        #return Response(UserSerializer(User.objects.all().order_by('?').first()).data, status=status.HTTP_200_OK)
        #return Response({"message": "get success!!"})

    # 유저 정보와 작성글 현황을 동시에 조회
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(request, username=username, password=password)
        
        
        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        #현재 유저의 id 값을 받는다.
        current_user_id = request.user.id

        current_user_info = UserSerializer(User.objects.get(id=current_user_id)).data
        current_user_articles = MyArticleSerializer(Article.objects.filter(user_id=current_user_id), many=True).data
        current_user_articles_count = len(current_user_articles)
        #현재 유저 정보, 작성글 수, 작성글을 return
        return Response({'유저 정보' : current_user_info,
                        '작성글 수' : current_user_articles_count,
                        '유저 작성글': current_user_articles},status=status.HTTP_200_OK)


class UserSignupApiView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        
        user_serializer = UserSerializer(data=request.data)

        if user_serializer.is_valid():
            # user_serializer.create() (X)
            # user_serializer.save() (O)

            # 왜 create() 가 아니고 save() 인지 알아보자!!
            user_serializer.save()
            return Response(user_serializer.data,status=status.HTTP_201_CREATED)
        

        return Response(user_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# JWT 갱신 확인용 API뷰
class LoginUserTokenAuthApi(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self,request):
       
        try:
            print(0)
            access_token = request.COOKIES['access_token']
            
            #payload = jwt.decode(access_token, env('DJANGO_SECRET_KEY'), algorithms=['HS256'])
            payload = jwt.decode(access_token, SIMPLE_JWT['SIGNING_KEY'], algorithms=[SIMPLE_JWT['ALGORITHM']])
            print(access_token)
            pk = payload.get('user_id')
            user = User.objects.get(id=pk)
            serializer = UserSerializer(user)
            response = Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
            response.set_cookie('access_token', access_token)
            response.set_cookie('refresh_token', request.COOKIES['refresh_token'])
            return response

        # 토큰 만료시 토큰 갱신
        except(jwt.exceptions.ExpiredSignatureError):
            print(0)
            try:
                # access 토큰 만료시
                serializer = TokenRefreshSerializer(data={'refresh': request.COOKIES.get('refresh_token', None)})

                if serializer.is_valid(raise_exception=True):
                    access_token = serializer.validated_data['access']
                    refresh_token = request.COOKIES.get('refresh_token', None)
                    # payload = jwt.decode(access_token, env('DJANGO_SECRET_KEY'), algorithms=['HS256'])
                    payload = jwt.decode(access_token, SIMPLE_JWT['SIGNING_KEY'], algorithms=[SIMPLE_JWT['ALGORITHM']])
                    pk = payload.get('user_id')
                    # user = get_user(pk)
                    user = User.objects.get(id=pk)
                    serializer = UserSerializer(instance=user)
                    response = Response(serializer.data, status=status.HTTP_200_OK)
                    response.set_cookie('access_token', access_token)
                    response.set_cookie('refresh_token', refresh_token)
                    return response
            except(rest_framework_simplejwt.exceptions.TokenError): # refresh 토큰까지 만료 시
                print(0)
                return Response({"message": "로그인이 만료되었습니다."}, status=status.HTTP_200_OK)

            raise jwt.exceptions.InvalidTokenError

        except(jwt.exceptions.InvalidTokenError): # 토큰 invalid 인 모든 경우
            return Response({"message": "로그인이 만료되었습니다."}, status=status.HTTP_200_OK)

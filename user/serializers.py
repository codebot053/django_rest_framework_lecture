from rest_framework import serializers

from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import Hobby as HobbyModel
from user.models import UseStack as UseStackModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        # password 가 추가되어야 하는 이유는 create, update 시 validation 을 제공하기 위함이다. 
        # password 는 Postman에서 API 로 노출되면 안되기에 read_only 처리를 해준다.
        fields = ['username', 'email', 'join_date', 'password', 'fullname']
        
        # 아래는 password 밑 다른 필드를 추가 처리하는 extra_kwargs 이다.
        extra_kwargs = {
            'password':{'write_only':True}, # write_only : 데이터를 쓰거나 생성하거나 검증할때만 사용한다.
        }
from rest_framework import serializers

from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import Hobby as HobbyModel
from user.models import UseStack as UseStackModel


# hobby serializer
class HobbySerializer(serializers.ModelSerializer):
    # 역참조, 나와 같은 hobby를 공유하는 사람들을 불러온다.
    '''
    same_hobby_person_field =serializers.SerializerMethodField()

    def get_same_hobby_person_field(self, obj):
        # obj는 조회된 유저의 취미 object를 받는다.
        print(f"{obj} / {type(obj)}")
        # 음악 / <class 'user.models.Hobby'> 
        # string 이 아닌 hobby라는 모델의 object 인것을 확인할 수 있다.
        # 모델 class 안에 있는 값이다. models.py에서 
        # class Hobby(models.Model): 에서
        # __str__(self) 를 비활성 하면 hobby object(num)이 출력되는것을 확인할 수 있다.
        return "good_serializer"
    '''
    same_hobby_users = serializers.SerializerMethodField()
    
    def get_same_hobby_users(self, obj):
        same_user_list = []
        #할수 있는 것들 표시 'dir'
        # print(dir(obj))
        # print(obj.userprofile_set.all())
        for user_profile in obj.userprofile_set.all():
            # 취미는 유저프로필의 foreign key 이므로 프로필에 유저에 풀네임으로 참조
            same_user_list.append(user_profile.user.fullname)
        return same_user_list
        '''
        "same_hobby_users": [
                    "지훈박",
                    "qwer",
                    "testuser0",
                    "admin"
                ]
        위와 같은 형태로 postman 에서 확인할수 있다.
        '''
    class Meta:
        model = HobbyModel
        fields = ['name','same_hobby_users']

# userprofile serializer
class UserProfileSerializer(serializers.ModelSerializer):
    # hobby serializer 등록
    # 만약 불러오는게 many to many 관계라면 'many=True'를 준다.
    # many to many 필드는 queryset 과 유사함.  그냥 불러오면 null값 return
    hobby = HobbySerializer(many=True)
    class Meta:
        model = UserProfileModel
        fields = ['introduction', 'age', 'birthday','hobby']    

class UserSerializer(serializers.ModelSerializer):
    # 위에 등록된 userprofile serializer를 가져온다.
    # 아래 코드를 지정하지 않으면 프로필 id가 리턴된다.
    # fields 에 마저 적어주기!
    userprofile = UserProfileSerializer()

    class Meta:
        model = UserModel
        # password 가 추가되어야 하는 이유는 create, update 시 validation 을 제공하기 위함이다. 
        # password 는 Postman에서 API 로 노출되면 안되기에 read_only 처리를 해준다.
        # fields = "__all__" 의 경우 전체 query를 불러올 수 있지만
        # 필요없는 데이터들이 많아 자주 사용하지는 않는다.
        fields = ['username', 'email', 'join_date', 'password', 'fullname', 'userprofile']

        # 아래는 password 밑 다른 필드를 추가 처리하는 extra_kwargs 이다.
        extra_kwargs = {
            'password':{'write_only':True}, # write_only : 데이터를 쓰거나 생성하거나 검증할때만 사용한다.
        }


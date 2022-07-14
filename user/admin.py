from django.contrib import admin
from django.contrib.auth.models import Group
from user.models import User
from user.models import UserProfile
from user.models import Hobby as UserHobbyList
# from user.models import UseStack as UserUseStackList
# Register your models here.

# Unregister Group
admin.site.unregister(Group)

# class IDShowAdminList(admin.ModelAdmin):
#     # list 또는 튜플 형태로 지정해야 한다. ex) ('id') X
#     # 하나일 경우 ('id',)였나??? 알아볼것
#     # ('id') 는 튜플이 아니다 ('id')는 튜플 이건 python syntax
#     list_display = ('id', 'name')

# 각기 다른 테이블 User , UserProfile 이지만 아래 클래스를 상속 받으면 
# 한 테이블 안의 상세 페이지에서 조회할수 있다. 
# StackedInline 상속시 세로로 조회
# TabulaInline 상속시 가로로 조회
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    
    # 만약 특정 objects를 제한적으로 보여주고 싶을경우 아래 코드를 사용한다. 
    # 지금의 경우 user 상세 페이지의 profile field에서 hobby id 값이 2 이하인 경우만 출력된다.
    # 2 이상의 id object는 조회불가.
    # 만약 hobby 테이블에 상세 카테고리 그리고 그 하위에 object가 있다면
    # kwargs['queryset'] = UserHobbyList.objects.filter(category='sports')
    # 이렇게 sports 카테고리에 해당하는 것들만 출력할수도 있다. 
    # 즉, 내가 원하는 데이터만 필터를 걸어 출력하는것.
    '''
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'hobby':
            # id__lte = 7 ==> less then or equal,7보다작거나 같은경우, 2이하
            kwargs['queryset'] = UserHobbyList.objects.filter(id__lte=2)
        # super() 를 쓰지않으면 부모class의 상속내용을 쓰는게 아니라 덮어쓰기 overwriting이 된다.
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    '''
# admin 심화 설정!
# 튜플이나 리스트로 넣어야 한다.
class UserAdmin(admin.ModelAdmin):
    # 사용자 목록에 보여질 필드지정
    list_display = ('id', 'username', 'fullname')
    # 아래 링크 설정 안할경우 Default로 'id'만 link 적용
    list_display_links = ('id','username')
    # db에 중복된 data가 있을경우 list_filter를 통해 중복된 내용을 필터로
    # 묶어서 볼 수 있다.
    list_filter = ('username',)
    # admin 에서 아래 칼럼들을 찾기 필드에 추가해 데이터로 찾아볼수 있다.
    search_fields = ('username','fullname')
    # read only로 설정할 필드 지정, 가입일의 경우 auto_now, auto_now_add로
    # 지정된 경우 default로 read only이지만 아래 필드에 추가되어야 상세 페이지에서
    # 볼 수 있다.
    readonly_fields = ('username','join_date')

    # 상세 페이지에서 필드를 종류별로 분류할떄 좋다.
    fieldsets = (
        ("info", {'fields': ('username', 'fullname', 'join_date','password')}),
        ('permissions', {'fields': ('is_admin', 'is_active', )}),
    )
    # 위에 생성한 UserProfileInline을 이제 유저 상세에서 볼수 있도록 등록.
    inlines = (
        UserProfileInline,
        )
admin.site.register(User, UserAdmin)
# UserProfile을 User 테이블 상세에서 StackInline처리 하였기에 잠시 주석처리.
#admin.site.register(UserProfile)
admin.site.register(UserHobbyList)
# admin.site.register(UserUseStackList)

from django.contrib import admin
from django.contrib.auth.models import Group
from user.models import User
from user.models import UserProfile
from user.models import Hobby as UserHobbyList
from user.models import UseStack as UserUseStackList
# Register your models here.

# Unregister Group
admin.site.unregister(Group)

class IDShowAdminList(admin.ModelAdmin):
    # list 또는 튜플 형태로 지정해야 한다. ex) ('id') X
    list_display = ('id', 'name')
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(UserHobbyList)
admin.site.register(UserUseStackList)

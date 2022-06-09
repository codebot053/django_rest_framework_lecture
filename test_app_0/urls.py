from django.urls import path
from . import views

app_name = 'test_app_0'

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
]
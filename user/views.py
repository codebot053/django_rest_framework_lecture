from xmlrpc.client import ResponseError
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.


class UserApi(APIView):
    # permission_classes
    def get(self, request):
        return Response({"message": "get success!"})
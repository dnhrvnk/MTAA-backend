from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from . import models
import json

def validateFields(data):
    if ('name' not in data or data['name'] == '' or
        'password' not in data or data['password'] == ''):
        return False
    return True

@api_view(['POST'])
def registerUser(request):
    registerData = request.data
    if not validateFields(registerData):
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    if models.Users.objects.filter(username__iexact=registerData['name']).exists():
        return Response(status=status.HTTP_409_CONFLICT)

    user = models.Users(username=registerData['name'],password=registerData['password'],displayName=registerData['name'])
    user.save()
    token = Token.objects.create(user=user)
    return Response({"id" : user.id, "token" : token.key}, status=status.HTTP_201_CREATED)
    


@api_view(['POST'])
def longinUser(request):
    if not validateFields(request.data):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    userQ = models.Users.objects.filter(username__iexact=request.data['name'], password=request.data['password'])
    if not userQ.exists():
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    user = userQ.get()
    token, created = Token.objects.get_or_create(user=user)
    return Response({
            'user_id': user.pk,
            'token': token.key
        })


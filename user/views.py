from numpy import empty
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
import json
from datetime import datetime
from django.db.models import Q
import uuid
from user.models import userBasicInfo, User

#TODO add photos

class userSerialize(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

def is_valid_uuid(id):
    try:
        uuid.UUID(str(id))
        return True
    except ValueError:
        return False


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def modifyUser(request):
    user = userBasicInfo.objects.get(id=request.user.id)
    for key,val in request.data.items():
        if key == 'username' or key == 'password':
            return Response(status=status.HTTP_403_FORBIDDEN)
        if key == 'displayName':
            if val == '':
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            user.displayName = val
        if key == 'bio':
            user.bio = val if val != "" else None
        if key == 'photo':
            user.photoPath.delete()
            ext = val.name.split('.')[-1]
            val.name = '{:}.{:}'.format(user.id,ext)
            user.photoPath = val
    user.save()
        
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def getInfo(request):
    q = request.GET.get('q','')
    if not is_valid_uuid(q):                                    #????
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = User.objects.filter(Q(id=q))
    if user:
        return Response(userSerialize(user, many = True, context = {'request': request}).data)
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def getGroups(request):
    ...

@api_view(['GET'])
def getBooks(request):
    ...

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def bookTolibrary(request):
    ...

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def bookFromLibrary(request):
    ...
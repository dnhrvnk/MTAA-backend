from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from . import models
import json

from datetime import datetime


#TODO add photos

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def modifyUser(request):
    user = models.userBasicInfo.objects.get(id=request.user.id)
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
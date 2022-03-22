from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from . import models
from PIL import Image

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def modifyUser(request):
    user = models.userBasicInfo.objects.get(id=request.user.id)
    for key,val in request.data.items():
        if key == 'username' or key == 'password' or (key == 'displayName' and val == ''):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        if key == 'displayName':
            user.displayName = val
        if key == 'bio':
            user.bio = val if val != "" else None
        if key == 'photo':
            user.photoPath.delete()
            ext = val.name.split('.')[-1]
            val.name = '{:}.{:}'.format(user.id,ext)
            user.photoPath = val
            try:
                im = Image.open(user.photoPath)
                im.verify()
            except:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    user.save()
        
    return Response(status=status.HTTP_200_OK)
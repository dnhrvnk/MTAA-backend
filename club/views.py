import stat
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from . import models,serializer
from django.db.models import Q
from PIL import Image


def __getSerializableClubInfo(clubID):
    club = models.Club.objects.get(id=clubID)
    users = models.User_Club.objects.filter(club=club)
    serUsers = []
    for i in users:
        user = models.userBasicInfo.objects.get(id=i.user.id)
        serUsers.append(models.serializableUser(user.id,user.displayName,user.photoPath,i.owner,i.joined))
    if hasattr(club,'book_of_the_week'):
        bow = club.book_of_the_week
        serAuthors = []
        for a in bow.author.all():
            serAuthors.append(a.name)
        bow = models.serializabeBook(bow.id,bow.title,serAuthors,bow.genre,bow.pages,bow.cover_path)
    else:
        bow = None
    serBooks = []
    for i in club.books.all().distinct():
        serAuthors = []
        for a in i.author.all():
            serAuthors.append(a.name)
        serBooks.append(models.serializabeBook(i.id,i.title,serAuthors,models.Genre.objects.get(id=i.genre.id).name,i.pages,i.cover_path))
    serClub = models.SerializableClub(club.id,club.name,club.info,club.rules,bow,serBooks,serUsers,club.photoPath)

    return serClub

    

@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def createGroup(request):
    if 'name' not in request.data or request.data['name'] == '':
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    if models.Club.objects.filter(name=request.data['name']).exists():
        return Response(status=status.HTTP_409_CONFLICT)
    
    club = models.Club(name=request.data['name'])
    user = models.userBasicInfo.objects.get(id=request.user.id)
    user_club = models.User_Club(user=user,club=club,owner=True)
    club.save()
    user_club.save()
    return Response(serializer.ClubSerializer(__getSerializableClubInfo(id),many=False,context={'request': request}).data,status=status.HTTP_201_CREATED)


@api_view(['GET'])
def getClubInfo(request,id):
    if not models.Club.objects.filter(id=id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    info = models.Club.objects.get(id=id)
    print(info.name)
    se = serializer.ClubSerializer(__getSerializableClubInfo(id),many=False,context={'request': request})
    return Response(se.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated,])
def joinClub(request,id):
    user = models.userBasicInfo.objects.get(id=request.user.id)
    if not models.Club.objects.filter(id=id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    if models.User_Club.objects.filter(club=id,user=user).exists():
        return Response(status=status.HTTP_409_CONFLICT)
    club = models.Club.objects.get(id=id)
    user_club = models.User_Club(user=user,club=club,owner=False)
    user_club.save()
    return Response(serializer.ClubSerializer(__getSerializableClubInfo(id),context={'request': request}).data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated,])
def leaveClub(request,id):
    user = models.userBasicInfo.objects.get(id=request.user.id)
    if not models.Club.objects.filter(id=id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    if not models.User_Club.objects.filter(club=id,user=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    if not models.User_Club.objects.filter(club=id,user=user.id).exists():
        return Response(status=status.HTTP_403_FORBIDDEN)
    club_user = models.User_Club.objects.get(club=id,user=user)
    if club_user.owner:
        return Response(status=status.HTTP_403_FORBIDDEN)
    club_user.delete()
    return Response(serializer.ClubSerializer(__getSerializableClubInfo(id),context={'request': request}).data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated,])
def deleteGroup(request,id):
    user = models.userBasicInfo.objects.get(id=request.user.id)
    if not models.Club.objects.filter(id=id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    if not models.User_Club.objects.filter(club=id,user=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    if not models.User_Club.objects.filter(club=id,user=user.id).exists():
        return Response(status=status.HTTP_403_FORBIDDEN)
    club_user = models.User_Club.objects.get(club=id,user=user)
    if not club_user.owner:
        return Response(status=status.HTTP_403_FORBIDDEN)
    models.Club.objects.get(id=id).delete()
    return Response()


@api_view(['PUT'])
@permission_classes([IsAuthenticated,])
def addBook(request,id):
    user = models.userBasicInfo.objects.get(id=request.user.id)
    q = request.GET.get('q','')
    if not models.Club.objects.filter(id=id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    if not models.Book.objects.filter(id=q).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    if not models.User_Club.objects.filter(club=id,user=user.id).exists():
        return Response(status=status.HTTP_403_FORBIDDEN)
    club_user = models.User_Club.objects.get(club=id,user=user.id)
    if not club_user.owner:
        return Response(status=status.HTTP_403_FORBIDDEN)

    club = models.Club.objects.get(id=id)
    book = models.Book.objects.get(id=q)
    club.book_of_the_week = book
    club.books.add(book)
    club.save()
    return Response(serializer.ClubSerializer(__getSerializableClubInfo(id),many=False,context={'request': request}).data)




@api_view(['PUT'])
@permission_classes([IsAuthenticated,])
def modifyGroup(request,id):
    user = models.userBasicInfo.objects.get(id=request.user.id)

    if not models.Club.objects.filter(id=id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    if not models.User_Club.objects.filter(club=id,user=user.id).exists():
        return Response(status=status.HTTP_403_FORBIDDEN)
    club_user = models.User_Club.objects.get(club=id,user=user.id)
    if not club_user.owner:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    club = models.Club.objects.get(id=id)
    for key,val in request.data.items():
        if key == 'name':
            if  val == '':
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            if models.Club.objects.filter(~Q(id=id),name__iexact=val).exists():
                return Response(status=status.HTTP_409_CONFLICT)
            club.name = val
        elif key == 'info':
            club.info = val if val != "" else None
        elif key == 'rules':
            club.rules = val if val != "" else None
        elif key == 'photo':
            club.photoPath.delete()
            ext = val.name.split('.')[-1]
            val.name = '{:}.{:}'.format(user.id,ext)
            club.photoPath = val
            try:
                im = Image.open(club.photoPath)
                im.verify()
            except:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    club.save()

    return Response(serializer.ClubSerializer(__getSerializableClubInfo(id),many=False,context={'request': request}).data)

@api_view(['DeLETE'])
@permission_classes([IsAuthenticated,])
def removeMember(request,id):
    user = models.userBasicInfo.objects.get(id=request.user.id)
    q = request.GET.get('q','')

    if not models.userBasicInfo.objects.filter(id=q).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    if not models.Club.objects.filter(id=id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    if not models.User_Club.objects.filter(club=id,user=user.id).exists():
        return Response(status=status.HTTP_403_FORBIDDEN)
    club_user = models.User_Club.objects.get(club=id,user=user.id)
    if not club_user.owner:
        return Response(status=status.HTTP_403_FORBIDDEN)
        
    if not models.User_Club.objects.filter(club=id,user=q).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    if models.User_Club.objects.get(club=id,user=q).owner:
        return Response(status=status.HTTP_403_FORBIDDEN)
    models.User_Club.objects.filter(club=id,user=q).delete()
    return Response(serializer.ClubSerializer(__getSerializableClubInfo(id),many=False,context={'request': request}).data)


    


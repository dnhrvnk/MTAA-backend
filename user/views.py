from email.policy import HTTP
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from datetime import datetime
from django.db.models import Q
import uuid
from modely.models import *
from .models import serializabeBook,serializableUser,SerializableClub
from rest_framework.views import APIView
from club.serializer import  ClubSerializer
from club.views import getSerializableClubInfo
from PIL import Image

class bookSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    cover = serializers.ImageField()

class clubSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=200)
    photoPath = serializers.ImageField(use_url=True)

class userSerialize(serializers.Serializer):
    id = serializers.UUIDField()
    displayName = serializers.CharField()
    photoPath = serializers.ImageField(use_url=True)
    wishlist = serializers.IntegerField()
    currently_reading = serializers.IntegerField()
    completed = serializers.IntegerField()
    recommended_books = serializers.ListField(
        child=bookSerializer()
    )
    clubs = serializers.ListField(
        child=clubSerializer()
    )

def is_valid_uuid(id):
    try:
        uuid.UUID(str(id))
        return True
    except ValueError:
        return False

def serializeClubs(clubs):
    serlz_clubs = []
    for i in clubs:
        club = i.club
        serlz_clubs.append(SerializableClub(club.id, club.name, club.info, club.rules, club.book_of_the_week, None, None, club.photoPath))
    return serlz_clubs

def serializeUser(user):
    wishlistC = user_books.objects.filter(user=user,status=Status.objects.get(id=1)).count()
    currently_readC = user_books.objects.filter(user=user,status=Status.objects.get(id=2)).count()
    completedC = user_books.objects.filter(user=user,status=Status.objects.get(id=3)).count()
    recommended = user_books.objects.filter(user=user,recommended=True)
    recommendedBooks = []
    for i in recommended.all():
        book = i.book
        recommendedBooks.append(serializabeBook(book.id,book.title,book.cover_path))
    clubs = []
    for i in User_Club.objects.filter(user=user):
        club = i.club
        clubs.append(SerializableClub(club.id,club.name,club.photoPath))
    return serializableUser(user.id,user.displayName, user.photoPath, wishlistC, currently_readC, completedC,recommendedBooks,clubs)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def modifyUser(request):
    user = User.objects.get(id=request.user.id)
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
            if not 'user.png' in user.photoPath.name:
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
        
    return Response(userSerialize(serializeUser(user), context = {'request': request}).data,status=status.HTTP_200_OK)

@api_view(['GET'])
def getInfo(request):
    q = request.GET.get('q','')
    if not is_valid_uuid(q):                                    
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(id=q)
    if user:
        return Response(userSerialize(serializeUser(user), context = {'request': request}).data)
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def getGroups(request):
    q = request.GET.get('q','')
    if not is_valid_uuid(q):                                    
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(id=q)
    clubs = []
    for club in User_Club.objects.filter(user=user):
        clubs.append(getSerializableClubInfo(club.club.id))
    return Response(ClubSerializer(clubs, context = {'request': request},many=True).data)

@api_view(['GET'])
def getBooks(request, list):
    user = User.objects.get(id=request.user.id)
    if list == '' or not Status.objects.filter(status_text = list).exists(): 
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    
    zoznam = []
    books = user_books.objects.filter(user = user, status = Status.objects.get(id = list))


    
class BookList(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request,isbn):
        user = User.objects.get(id=request.user.id)
        q = request.GET.get('q','')
        if q == '' or (not Status.objects.filter(status_text=q).exists() and q != 'recommend' and q != 'unrecommend'): 
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        if not Book.objects.filter(id=isbn).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        if q == 'unrecommend' and not user_books.objects.filter(user = user, book = Book.objects.get(id = isbn)).exists():
            return Response(status=status.HTTP_409_CONFLICT)

        userBook,created = user_books.objects.get_or_create(user=user,book=Book.objects.get(id=isbn))
        if q == 'recommend':
            userBook.recommended = True
            userBook.save()
        elif q == 'unrecommend':
            if not hasattr(userBook,'status'):
                user_books.objects.filter(user = user, book = Book.objects.get(id = isbn)).delete()
            else:
                userBook.recommended = False
                userBook.save()
        elif Status.objects.filter(status_text = q).exists():
            if hasattr(userBook,'status') and userBook.status == Status.objects.get(status_text = q): 
                return Response(status=status.HTTP_409_CONFLICT)
            userBook.status = Status.objects.get(status_text = q)
            userBook.started = datetime.now()
            userBook.save()

        return Response(userSerialize(serializeUser(user), context = {'request': request}).data)

    def delete(self, request,isbn):
        user = User.objects.get(id = request.user.id)
        if not Book.objects.filter(id = isbn).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not user_books.objects.filter(user = user, book = Book.objects.get(id=isbn)).exists():
            return Response(status=status.HTTP_409_CONFLICT)
        userBook = user_books.objects.get(user = user, book = Book.objects.get(id=isbn)) 
        if userBook.recommended == True:
            userBook.status = None
            userBook.save()
        else:
            user_books.objects.filter(user = user, book = Book.objects.get(id=isbn)).delete()

        return Response(userSerialize(serializeUser(user), context = {'request': request}).data)
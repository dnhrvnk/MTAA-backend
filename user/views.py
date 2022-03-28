from doctest import DocFileSuite
from xmlrpc.client import boolean
from numpy import number
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
import uuid
from modely.models import *
from .models import *
from rest_framework.views import APIView
from PIL import Image
from django.core.exceptions import ObjectDoesNotExist
from user.serializer import *

def is_valid_uuid(id):
    try:
        uuid.UUID(str(id))
        return True
    except ValueError:
        return False

def serializeClubs(clubs, cl:boolean = False):
    serlz_clubs = []
    for i in clubs:
        club = i if cl else i.club
        number_of_members = User_Club.objects.filter(club_id = club.id).count()
        serlz_clubs.append(serializableClub(club.id, club.name, club.photoPath, number_of_members))
    return serlz_clubs

def serializeLibrary(books):
    serlz_books = []
    for i in books:
        book = i.book
        serlz_books.append(serializableLibrary(book.id, book.title, book.description, book.cover_path))
    return serlz_books

def serializeRecommendedBooks(recommended, books:boolean = False):
    recommendedBooks = []
    for i in recommended.all():
        book = i if books else i.book
        recommendedBooks.append(serializableBook(book.id, book.title, book.cover_path))
    return recommendedBooks

def serializeUser(user):
    wishlistC = user_books.objects.filter(user = user, status = Status.objects.get(id = 1)).count()
    currently_readC = user_books.objects.filter(user = user, status = Status.objects.get(id = 2)).count()
    completedC = user_books.objects.filter(user = user, status = Status.objects.get(id = 3)).count()
    recommendedBooks = serializeRecommendedBooks(user_books.objects.filter(user = user, recommended = True))
    clubs = serializeClubs(User_Club.objects.filter(user = user))
    return serializableUser(user.id, user.displayName, user.photoPath, wishlistC, currently_readC, completedC, recommendedBooks, clubs)

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
        
    return Response(userSerializer(serializeUser(user), context = {'request': request}).data,status=status.HTTP_200_OK)

@api_view(['GET'])
def getInfo(request):
    q = request.GET.get('q','')
    if not is_valid_uuid(q): return Response(status = status.HTTP_404_NOT_FOUND)    

    try:
        user = User.objects.get(id = q)
        return Response(userSerializer(serializeUser(user), context = {'request': request}).data)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def getGroups(request):
    q = request.GET.get('q','')
    if not is_valid_uuid(q): return Response(status = status.HTTP_404_NOT_FOUND)    
    
    try:
        user = User.objects.get(id = q)
        clubs = serializeClubs(User_Club.objects.filter(user = user))
        return Response(clubSerializer(clubs, context = {'request': request}, many = True).data)
    except ObjectDoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def getBooks(request, list):
    q = request.GET.get('q','')
    if not is_valid_uuid(q): return Response(status = status.HTTP_404_NOT_FOUND)  

    try:
        user = User.objects.get(id = q)
        if list == '' or not Status.objects.filter(status_text = list).exists(): 
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)                  #zle zadany {list}
            
        books = serializeLibrary(user_books.objects.filter(user = user, status = Status.objects.get(status_text = list)))
        return Response(librarySerializer(books, context = {'request': request}, many = True).data)
    except ObjectDoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
class BookList(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, isbn):
        user = User.objects.get(id = request.user.id)
        q = request.GET.get('q', '')
        q = q.lower()
        if q == '' or (not Status.objects.filter(status_text = q).exists() and q != 'recommend' and q != 'unrecommend'):   
            return Response(status = status.HTTP_406_NOT_ACCEPTABLE)                                                            #nebol zadany spravny {list}
        if not Book.objects.filter(id = isbn).exists():
            return Response(status = status.HTTP_404_NOT_FOUND)                                                                 #kniha neexistuje
        if q == 'unrecommend' and not user_books.objects.filter(user = user, book = Book.objects.get(id = isbn)).exists():      
            return Response(status=status.HTTP_409_CONFLICT)                                                                    #spojenie kniha-pouzivatel neexistuje

        userBook, created = user_books.objects.get_or_create(user = user, book = Book.objects.get(id = isbn))
        if q == 'recommend':
            if userBook.recommended == True: return Response(status = status.HTTP_409_CONFLICT)                                 #kniha uz je recommended
            userBook.recommended = True
            userBook.save()
        elif q == 'unrecommend':
            if userBook.recommended == False or userBook.recommended == None: 
                return Response(status = status.HTTP_409_CONFLICT)                                              #kniha nie je recommended alebo je uz unrecommended
            if not hasattr(userBook,'status'):                                                      
                user_books.objects.filter(user = user, book = Book.objects.get(id = isbn)).delete()             #nie je v kniznici --> vymaaze sa zaznam
            else:
                userBook.recommended = False                                                                    #je v kniznici --> len sa unrecommend-ne
                userBook.save()
        elif Status.objects.filter(status_text = q).exists():
            if hasattr(userBook, 'status') and userBook.status == Status.objects.get(status_text = q): 
                return Response(status = status.HTTP_409_CONFLICT)                                              #kniha uz je v danej kategorii kniznice
            userBook.status = Status.objects.get(status_text = q)
            userBook.started = datetime.now()
            userBook.save()

        return Response(userSerializer(serializeUser(user), context = {'request': request}).data)

    permission_classes = [IsAuthenticated]
    def delete(self, request, isbn):
        user = User.objects.get(id = request.user.id)
        if not Book.objects.filter(id = isbn).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)                                               #pozadovana kniha neexistuje
        if not user_books.objects.filter(user = user, book = Book.objects.get(id = isbn)).exists():
            return Response(status=status.HTTP_409_CONFLICT)                                                #spojenie kniha-pouzivatel neexistuje
        
        userBook = user_books.objects.get(user = user, book = Book.objects.get(id = isbn))
        if userBook.status_id == None and userBook.recommended == True:                                     
            return Response(status=status.HTTP_409_CONFLICT)                                                #pouzivatel nema knihu v kniznici, len v recommended

        if userBook.recommended == True:                                                                    #ak ma knihu v kniznici a aj v recommended
            userBook.status = None                                                                          #vymaze ju z kniznice, ale zaznam o recommended zostava
            userBook.save()
        else:
            user_books.objects.filter(user = user, book = Book.objects.get(id = isbn)).delete()             #ak ju nema v recommended, tak vymaze sa vsetko

        return Response(userSerializer(serializeUser(user), context = {'request': request}).data)
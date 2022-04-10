from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from search.serializer import bookSerializer

from user.models import *
from search.models import *
from user.views import serializeClubs, serializeRecommendedBooks
from user.serializer import clubSerializer
from search.serializer import bookFindSerializer
import random

def serializeBook(book):
    rating = round(random.uniform(1.00, 5.00), 2)
    readers = user_books.objects.filter(status=Status.objects.get(id = 2)).count() +  user_books.objects.filter(status=Status.objects.get(id = 3)).count()

    return serializableBookInfo(book.id, book.title, book.author, book.genre, book.pages, book.description, book.cover_path, readers, rating)

@api_view(['GET'])
def getBooks(request):
    q = request.GET.get('q','')
    books = serializeRecommendedBooks(Book.objects.filter(Q(title__icontains = q) | Q(author__name__icontains = q)), True)
    return Response(bookFindSerializer(books, context = {'request': request}, many = True).data)
 
@api_view(['GET'])
def getClubs(request):
    q = request.GET.get('q','')
    clubs = serializeClubs(Club.objects.filter(Q(name__icontains = q)), True)
    return Response(clubSerializer(clubs, context = {'request': request}, many = True).data)

@api_view(['GET'])
def getInfo(request, isbn):
    if not Book.objects.filter(id = isbn).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    book = Book.objects.get(id = isbn)
    return Response(bookSerializer(serializeBook(book), context = {'request': request}).data)
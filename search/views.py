from dataclasses import field
from unicodedata import name
from django.db import models
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q

from modely.models import *


class AuthorSerialize(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class genreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields= '__all__'

class bookSerialize(serializers.ModelSerializer):
    genre = genreSerializer()
    author = AuthorSerialize(source='get_author',many=True)
    class Meta:
        model = Book
        fields = '__all__'

class clubSerialize(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = '__all__'

@api_view(['GET'])
def testGet(response):
    items = Author.objects.all()
    for e in items:
        print(e.name)
    return Response(AuthorSerialize(items,many=True).data)


    

@api_view(['GET'])
def getBooks(request):
    q = request.GET.get('q','')
    books = Book.objects.filter(Q(title__contains=q) | Q(author__name__contains=q))
    return Response(bookSerialize(books,many=True,context={'request': request}).data)

@api_view(['GET'])
def getClubs(request):
    q = request.GET.get('q','')
    clubs = Club.objects.filter(Q(name__contains=q))
    return Response(bookSerialize(clubs, many=True, context={'request': request}).data)
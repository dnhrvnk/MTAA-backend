from rest_framework import serializers
from club.models import Club, User_Club,SerializableClub
from search.models import Book
from user.models import userBasicInfo
import uuid

class BookSeriliazer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    author = serializers.ListField(
        child=serializers.CharField()
    )
    genre = serializers.CharField()
    pages = serializers.IntegerField()
    cover = serializers.ImageField()
 
class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    displayName = serializers.CharField()
    photoPath = serializers.ImageField(use_url=True)
    owner = serializers.BooleanField()
    joined = serializers.DateTimeField()

class ClubSerializer(serializers.Serializer):   
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=200)
    info = serializers.CharField()
    rules = serializers.CharField()
    photoPath = serializers.ImageField(use_url=True)
    count = serializers.IntegerField()
    users= serializers.ListField(
        child=UserSerializer()
    )
    book_of_the_week = BookSeriliazer()
    book_count = serializers.IntegerField()
    books = serializers.ListField(
        child= BookSeriliazer()
    )
    class Meta:
        model=SerializableClub
        fields = '__all__'

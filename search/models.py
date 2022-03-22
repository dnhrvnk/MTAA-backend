from django.db import models
from rest_framework import serializers
from django.contrib.auth.base_user import AbstractBaseUser
import uuid


class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    color = models.IntegerField()

    class Meta:
        managed=False
        db_table = 'genres'

class Author(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    class Meta:
        managed=False
        db_table = 'authors'

class Book(models.Model):
    id = models.CharField(unique=True,primary_key=True,editable=False, max_length=20)
    title = models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    description = models.TextField()
    pages = models.IntegerField()
    cover_path = models.ImageField(upload_to='data/books')
    author = models.ManyToManyField(Author,db_table='book_author')

    def get_author(self):
        return Author.objects.filter(book=self)
        
    class Meta:
        managed=False
        db_table = 'books'


class Club(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    info = models.TextField() 
    rules = models.TextField()
    photoPath = models.ImageField(upload_to='data/clubs')
    
    book_of_the_week = models.ManyToManyField(Book, db_table='club_books')
    #chyba clenovia
        
    class Meta:
        managed=False
        db_table = 'clubs'
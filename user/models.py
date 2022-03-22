from django.db import models
from rest_framework import serializers
from django.contrib.auth.base_user import AbstractBaseUser
import uuid

class userBasicInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    displayName = models.CharField(max_length=200)
    bio = models.TextField()
    photoPath = models.ImageField(upload_to='data/users')

    class Meta:
        managed = False
        db_table = 'users'

class Status(models.Model):
    id = models.CharField(unique=True,primary_key=True,editable=False, max_length=20)
    status_text = models.TextField()

    class Meta:
        managed = False
        db_table = 'status'

class Book(models.Model):
    id = models.CharField(unique=True,primary_key=True,editable=False, max_length=20)
    title = models.TextField()
    cover_path = models.ImageField(upload_to='data/books')
    status = models.ManyToManyField(Status, db_table='user_books') 

    def get_status(self):
        return Status.objects.filter(book=self)

    class Meta:
        managed = False
        db_table = 'books'

class Club(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    photoPath = models.ImageField(upload_to='data/clubs')
        
    class Meta:
        managed = False
        db_table = 'clubs'

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    displayName = models.CharField(max_length=200)
    bio = models.TextField()
    photoPath = models.ImageField(upload_to='data/users')
    
    recommended_books = models.ManyToManyField(Book, db_table='user_books')         #treba dorobit aby to boli len tie recommended

    #for book in recommended_books:
    #    if book.recommended:
    #        recommended_books.remove(book)

    clubs = models.ManyToManyField(Club, db_table='user_club')
    wishlist = 0
    currently_reading = 0
    completed = 0
    """for book in recommended_books:
        if book.status == "wishlist":  wishlist += 1
        if book.status == "completed":  completed += 1
        if book.status == "currently_reading":  currently_reading += 1"""

    def get_books(self):
        return Book.objects.filter(user=self)

    def get_clubs(self):
        return Club.objects.filter(user=self)

    class Meta:
        managed = False
        db_table = 'users'
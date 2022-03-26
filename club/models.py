from django.db import models
from modely.models import *

class SerializableClub:
    def __init__(self,id,name,info,rules,book_of_the_week,books, users,photoPath):
        self.id = id
        self.name = name
        self.info = info
        self.rules = rules
        self.book_of_the_week = book_of_the_week
        self.books = books
        self.book_count = len(books)
        self.users = users
        self.photoPath = photoPath
        self.count = len(users)

class serializableUser:
    def __init__(self,id,displayName,photoPath,owner,joined):
        self.id = id
        self.displayName = displayName
        self.photoPath = photoPath
        self.owner = owner
        self.joined = joined

class serializabeBook:
    def __init__(self,id,title,author,genre,pages,cover):
        self.id = id
        self.title = title
        self.author = author
        self.genre = genre
        self.pages = pages
        self.cover = cover
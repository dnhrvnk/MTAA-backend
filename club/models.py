from django.db import models
import uuid
from search.models import Book,Genre
from user.models import userBasicInfo


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
        self.displayName= displayName
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

class Club(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200,unique=True,blank=False)
    info = models.TextField()
    rules = models.TextField()
    photoPath = models.ImageField(upload_to='data/groups')
    book_of_the_week = models.OneToOneField(Book,on_delete=models.PROTECT,db_column='book_of_the_week')
    books = models.ManyToManyField(Book,db_table='club_books',related_name='books')
    users=models.ManyToManyField(userBasicInfo,through='User_Club')
    class Meta:
        managed= False
        db_table = 'clubs'


class User_Club(models.Model):
    user = models.ForeignKey(userBasicInfo,on_delete=models.CASCADE,related_name='info')
    club = models.ForeignKey(Club,on_delete=models.CASCADE)
    owner = models.BooleanField(default=False)
    joined = models.DateTimeField(auto_now_add=True)
    class Meta:
        managed= False
        db_table = 'user_club'

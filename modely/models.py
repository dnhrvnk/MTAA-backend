from django.db import models
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


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    displayName = models.CharField(max_length=200)
    bio = models.TextField()
    photoPath = models.ImageField(upload_to='data/users',default='data/default/user.png')
    recommended_books = models.ManyToManyField(Book, through="user_books")         
    #clubs = models.ManyToManyField(Club, db_table='user_club')
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = False
        db_table = 'users'


class Club(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200,unique=True,blank=False)
    info = models.TextField()
    rules = models.TextField()
    photoPath = models.ImageField(upload_to='data/groups',default='data/default/user.png')
    book_of_the_week = models.OneToOneField(Book,on_delete=models.PROTECT,db_column='book_of_the_week',related_name='bow')
    books = models.ManyToManyField(Book,db_table='club_books',related_name='books')
    users=models.ManyToManyField(User,through='User_Club')
    class Meta:
        managed= False
        db_table = 'clubs'


class User_Club(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='info')
    club = models.ForeignKey(Club,on_delete=models.CASCADE)
    owner = models.BooleanField(default=False)
    joined = models.DateTimeField(auto_now_add=True)
    class Meta:
        managed= False
        db_table = 'user_club'


class Status(models.Model):
    id = models.CharField(unique=True,primary_key=True,editable=False, max_length=20)
    status_text = models.TextField()

    class Meta:
        managed = False
        db_table = 'status'

class user_books(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    status = models.ForeignKey(Status,on_delete=models.CASCADE)
    recommended = models.BooleanField()
    started = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_books'


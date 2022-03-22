from modely.models import *

class serializableUser:
    def __init__(self, id, displayName, photoPath, wishlist, currently_reading, completed,recommended, clubs):
        self.id = id
        self.displayName= displayName
        self.photoPath = photoPath
        self.wishlist = wishlist
        self.currently_reading = currently_reading
        self.completed = completed
        self.recommended_books = recommended
        self.clubs = clubs
        
class serializabeBook:
    def __init__(self,id,title,cover):
        self.id = id
        self.title = title
        self.cover = cover

class SerializableClub:
    def __init__(self,id,name,photoPath):
        self.id = id
        self.name = name
        self.photoPath = photoPath

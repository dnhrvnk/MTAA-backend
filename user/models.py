from modely.models import *

class serializableUser:
    def __init__(self, id, displayName, bio, photoPath, wishlist, currently_reading, completed,recommended, clubs):
        self.id = id
        self.displayName = displayName
        self.bio = bio
        self.photoPath = photoPath
        self.wishlist = wishlist
        self.currently_reading = currently_reading
        self.completed = completed
        self.recommended_books = recommended
        self.clubs = clubs
        
class serializableBook:
    def __init__(self, id, title, cover):
        self.id = id
        self.title = title
        self.cover = cover

class serializableClub:
    def __init__(self, id, name, photoPath, nm):
        self.id = id
        self.name = name
        self.number_of_members = nm
        self.photoPath = photoPath

class serializableLibrary:
    def __init__(self, id, title, description, cover):
        self.id = id
        self.title = title
        self.description = description[:255] + "..."
        self.cover_path = cover
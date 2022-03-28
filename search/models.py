
class serializableAuthor:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class serializableGenre:
    def __init__(self, id, name,color):
        self.id = id
        self.name = name
        self.color = color

class serializableBookInfo:
    def __init__(self, id, title, author, genre, pages, description, cover, readers, rating):
        self.id = id
        self.title = title

        serAuthors = []
        for a in author.all():
            serAuthors.append(serializableAuthor(a.id, a.name))
        self.author = serAuthors

        self.genre = serializableGenre(genre.id, genre.name,genre.color)
        self.pages = pages
        self.description = description
        self.number_of_readers = readers
        self.rating = rating
        self.cover = cover
from studiolib import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    e_mail = db.Column(db.String(64), index=True, unique=True)
    pw = db.Column(db.String(64))


    def __init__(self, pw, e_mail):
        self.pw = pw
        self.e_mail = e_mail

    def __repr__(self):
        return self.e_mail

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)



relation_table = db.Table('relation_table',
                          db.Column('author_id', db.Integer, db.ForeignKey('authors.id')),
                          db.Column('book_id', db.Integer, db.ForeignKey('books.id'))
                          )

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    books = db.relationship('Book', secondary=relation_table, backref=db.backref('authors', lazy='dynamic'), lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name
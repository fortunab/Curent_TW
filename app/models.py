from app import db
from flask_login import UserMixin
from sqlalchemy.exc import IntegrityError

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    lastn = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __init__(self, name, lastn, username, email, password):
        self.name = name
        self.lastn = lastn
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r - %s>' % (self.id) % (self.email)

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        return self

class Friend(UserMixin, db.Model):
    __tablename__ = 'friend'
    id_fr = db.Column(db.Integer, primary_key=True)
    username_friend = db.Column(db.String, nullable=False, unique=True)
    username_fk = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)

    def __init__(self, username_friend, username_fk):
        self.username_friend = username_friend
        self.username_fk = username_fk

    def __repr__(self):
        return '<Server %r>' % (self.id_fr)

    def save1(self):
        db.session.add(self)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        return self 

    def rmv(self):
        db.session.delete(self)
        db.session.commit()
        return self

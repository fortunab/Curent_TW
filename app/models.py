from app import db
from flask_login import UserMixin
from sqlalchemy.exc import IntegrityError

from sqlalchemy.inspection import inspect

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
    name_fr = db.Column(db.String, nullable=False)
    username_friend = db.Column(db.String, nullable=False, unique=True)
    username_fk = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)

    def __init__(self, name_fr, username_friend, username_fk):
        self.name_fr = name_fr
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


class Chat(UserMixin, db.Model):
    __tablename__ = 'chat'
    id_chat = db.Column(db.Integer, primary_key=True)
    user_pers1 = db.Column(db.String, nullable=False)
    user_pers2 = db.Column(db.String, nullable=False)

    def __init__(self, user_pers1, user_pers2):
        self.user_pers1 = user_pers1
        self.user_pers2 = user_pers2

    def __repr__(self):
        return '<Server %r>' % (self.id_chat)

    def save2(self):
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

class Message(db.Model):
    __tablename__ = 'message'

    id_mes = db.Column('id_mes', db.Integer, primary_key=True)
    username_mes = db.Column('username_mes', db.String, nullable=False)
    text_mes = db.Column('text_mes', db.String(500), nullable=False)
    dateTime = db.Column(db.DateTime, index=True, nullable=False)

    def __init__(self, username_mes, text_mes, dateTime):
        self.username_mes = username_mes
        self.text_mes = text_mes
        self.dateTime = dateTime

    def __repr__(self):
        return '<Message %r>' % self.id_mes

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        return self

class FileContinut(db.Model):
    __tablename__ = 'files'

    id_fc = db.Column('id_fc', db.Integer, primary_key=True)
    name_fc = db.Column('name_fc', db.String(500))
    data_fc = db.Column('data_fc', db.LargeBinary)

    def __init__(self, name_fc, data_fc):
        self.name_fc = name_fc
        self.data_fc = data_fc

    def __repr__(self):
        return '<Message %r>' % self.id_fc

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        return self

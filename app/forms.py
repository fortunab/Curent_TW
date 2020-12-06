from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired, Length, Required


class LoginForm(FlaskForm):
	username = StringField(u'Username', validators=[DataRequired(message='Parola sau nume de utilizator incorecte.')])
	password = PasswordField(u'Password', validators=[DataRequired(message='Parola sau nume de utilizator incorecte.')])

class RegisterForm(FlaskForm):
	name = StringField(u'Name', validators=[DataRequired()])
	lastn = StringField(u'Lastn', validators=[DataRequired()])
	username = StringField(u'Username', validators=[DataRequired(message='Enter a unique username.')])
	email = StringField(u'Email', validators=[DataRequired(), Email(message='Enter a valid email.')])
	password = PasswordField(u'Password', validators=[DataRequired(), Length(min=6, message='Select a stronger password.')])

class FriendForm(FlaskForm):
	name_fr = StringField(u'NameFr', validators=[DataRequired()])
	username_friend = StringField(u'username_friend', validators=[DataRequired()])
	username_fk = StringField(u'username_fk', validators=[DataRequired()])

class ConnectChatForm(FlaskForm):
	user_pers1 = StringField(u'UserPers1', validators=[DataRequired()])
	user_pers2 = StringField(u'UserPers1', validators=[DataRequired()])

class MessageForm(FlaskForm):
	username_mes = StringField(u'username_mes', validators=[DataRequired()])
	text_mes = StringField(u'text_mes', validators=[DataRequired()])

class RoomForm(FlaskForm):
	name = StringField('Name', validators=[Required()])
	room = StringField('Room', validators=[Required()])
	submit = SubmitField('Enter Chatroom')

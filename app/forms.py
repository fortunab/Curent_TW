from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired, Length

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
	username_friend = StringField(u'username_friend', validators=[DataRequired()])
	username_fk = StringField(u'username_fk', validators=[DataRequired()])

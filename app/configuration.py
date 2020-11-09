import os

# Preia directoarele in care ruleaza scripta
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
	CSRF_ENABLED = True
	SECRET_KEY = "diofla15#yobobo"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')

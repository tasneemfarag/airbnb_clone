from peewee import *
from base import db
from user import User
from review import Review

class ReviewUser(Model):

	class Meta:
		''' Connects the model to the DB '''
		database = db

	user = ForeignKeyField(rel_model=User)
	review = ForeignKeyField(rel_model=Review)

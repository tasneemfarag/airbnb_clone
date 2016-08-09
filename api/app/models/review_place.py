from peewee import *
from base import db
from place import Place
from review import Review

class ReviewPlace(Model):

	class Meta:
		''' Connects the model to the DB '''
		database = db

	place = ForeignKeyField(rel_model=Place)
	review = ForeignKeyField(rel_model=Review)

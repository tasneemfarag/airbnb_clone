from base import *
from place import Place
from amenity import Amenity

class PlaceAmenities(Model):
    ''' Model to create a join table between Places and Ammenities '''

    class Meta:
        ''' Connects the model to the DB '''
        database = db

    place = ForeignKeyField(rel_model=Place)
    amenity = ForeignKeyField(rel_model=Amenity)

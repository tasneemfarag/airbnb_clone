from base import *
from place import Place
from amenity import Amenity

class PlaceAmenities(Model):

    class Meta:
        database = db

    place = ForeignKeyField(rel_model=Place)
    amenity = ForeignKeyField(rel_model=Amenity)

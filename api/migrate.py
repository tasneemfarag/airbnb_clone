from app.models.base import db
from app.models.user import User
from app.models.city import City
from app.models.state import State
from app.models.place import Place
from app.models.place_book import PlaceBook
from app.models.amenity import Amenity
from app.models.place_amenity import PlaceAmenities

db.connect()
db.create_tables([User,State,City,Place,Amenity,PlaceBook,PlaceAmenities])
db.close()

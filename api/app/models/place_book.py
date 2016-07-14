from base import *
from place import Place
from user import User

class PlaceBook(BaseModel):
    place = ForeignKeyField(rel_model=Place)
    user = ForeignKeyField(rel_model=User, related_name="places_booked")
    is_validated = BooleanField(default=False)
    date_start = DateTimeField(null=False, formats="%Y/%m/%d %H:%M:%S")
    number_nights = IntegerField(default=1)

    def to_hash(self):
        ''' Returns a hash of a booking in the database '''
        data = {}
        place = Place.get(Place.id == self.place)
        user = User.get(User.id == self.user)
        data['place_id'] = place.id
        data['user_id'] = user.id
        data['is_validated'] = self.is_validated
        data['date_start'] = self.date_start.strftime("%Y/%m/%d %H:%M:%S")
        data['number_nights'] = self.number_nights
        return super(PlaceBook, self).to_hash(self, data)

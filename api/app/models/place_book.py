from base import *
from place import Place
from user import User

class PlaceBook(BaseModel):
    place = ForeignKeyField(rel_model=Place)
    user = ForeignKeyField(rel_model=User, related_name="places_booked")
    is_validated = BooleanField(default=False)
    date_start = DateTimeField(null=False)
    number_nights = IntegerField(default=1)

    def to_hash(self):
        data = {}
        data['id'] = self.id
        data['created_at'] = self.created_at
        data['updated_at'] = self.updated_at
        data['place_id'] = self.place
        data['user_id'] = self.user
        data['is_validated'] = self.is_validated
        data['date_start'] = self.date_start
        data['number_nights'] = self.number_nights
        return data

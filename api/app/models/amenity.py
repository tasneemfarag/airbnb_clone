from base import *

class Amenity(BaseModel):
    name = CharField(max_length=128, null=False)

    def to_hash(self):
        data = {}
        data['name'] = self.name
        return super(Amenity, self).to_hash(self, data)

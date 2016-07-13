from base import *

class State(BaseModel):
    name = CharField(max_length=128, null=False, unique=True)

    def to_hash(self):
        data = {}
        data['id'] = self.id
        data['created_at'] = self.created_at
        data['updated_at'] = self.updated_at
        data['name'] = self.name
        return data

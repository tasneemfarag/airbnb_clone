from base import *

class State(BaseModel):
    name = CharField(max_length=128, null=False, unique=True)

    def to_dict(self):
        ''' Returns a hash of the State in the database '''
        data = {}
        data['name'] = self.name
        return super(State, self).to_dict(self, data)

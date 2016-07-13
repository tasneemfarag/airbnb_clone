from base import *
from hashlib import *

class User(BaseModel):

    email = CharField(max_length=128, null=False, unique=True)
    password = CharField(max_length=128, null=False)
    first_name = CharField(max_length=128, null=False)
    last_name = CharField(max_length=128, null=False)
    is_admin = BooleanField(default=False)

    def set_password(self, clear_password):
        passwd = md5()
        passwd.update(clear_password)
        self.password = passwd.hexdigest()

    def to_hash(self):
        data = {}
        data['email'] = self.email
        data['first_name'] = self.first_name
        data['last_name'] = self.last_name
        data['is_admin'] = self.is_admin
        return super(User, self).to_hash(self, data)

from config import *
from peewee import *
from datetime import datetime

db = MySQLDatabase(host=DATABASE['host'],port=DATABASE['port'],user=DATABASE['user'],\
                   password=DATABASE['password'],database=DATABASE['database'])

class BaseModel(Model):
    id = PrimaryKeyField(unique = True)
    created_at = DateTimeField(default=datetime.now(),formats="%Y/%m/%d %H:%M:%S")
    updated_at = DateTimeField(default=datetime.now(),formats="%Y/%m/%d %H:%M:%S")

    def save(self, *args, **kwargs):
        ''' Saves the Model to the database '''
        self.updated_at = datetime.now()
        super(BaseModel, self).save()

    def to_dict(model, self, data):
        ''' Returns a hash of the BaseModel in the database '''
        data['id'] = self.id
        data['created_at'] = self.created_at.strftime("%Y/%m/%d %H:%M:%S")
        data['updated_at'] = self.updated_at.strftime("%Y/%m/%d %H:%M:%S")
        return data

    class Meta:
        ''' Connects to the database '''
        database = db
        order_by = ("id", )

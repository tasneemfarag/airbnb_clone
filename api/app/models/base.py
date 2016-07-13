from config import *
from peewee import *
from datetime import datetime

db = MySQLDatabase(host=DATABASE['host'],port=DATABASE['port'],user=DATABASE['user'],\
                  password=DATABASE['password'],database=DATABASE['database'])

class BaseModel(Model):
    id = PrimaryKeyField(unique = True)
    created_at = DateTimeField()
    updated_at = DateTimeField(default=datetime.now(),formats="%Y/%m/%d %H:%M:%S")

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        super(BaseModel, self).save()


    class Meta:
        database = db
        order_by = ("id", )

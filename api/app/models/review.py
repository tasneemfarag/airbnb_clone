from base import *
from user import User

class Review(BaseModel):

	message = TextField(null=False)
	stars = IntegerField(default=0)
	user = ForeignKeyField(rel_model=User, related_name="reviews", on_delete="CASCADE")

	def to_dict(self):
		''' Returns a hash of the Review in the database '''
		data = {}
		data['message'] = self.message
		data['stars'] = self.stars
		data['fromuserid'] = self.user_id
		if 'reviewuser' in dir(self):
			data['touserid'] = self.reviewuser.user_id
		else:
			data['touserid'] = None
		if 'reviewplace' in dir(self):
			data['toplaceid'] = self.reviewplace.place_id
		else:
			data['toplaceid'] = None
		return super(Review, self).to_dict(self, data)

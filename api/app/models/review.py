from base import *
from user import User

class Review(BaseModel):

	message = TextField(null=False)
	stars = IntegerField(default=0)
	user = ForeignKeyField(rel_model=User, related_name="reviews", on_delete="CASCADE")

	def to_dict(self):
		''' Returns a hash of the Review in the database '''
		user = User.get(User.id == self.user)
		data = {}
		data['message'] = self.message
		data['stars'] = self.stars
		data['fromuserid'] = user.id
		return super(Review, self).to_dict(self, data)

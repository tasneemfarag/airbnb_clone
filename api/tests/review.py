''' App import '''
from app import app

''' Model import '''
from app.models.base import db
from app.models.user import User
from app.models.review_user import ReviewUser
from app.models.review_place import ReviewPlace
from app.models.review import Review
from app.models.place import Place
from app.models.city import City
from app.models.state import State

''' Test data import '''
from review_data import *
from state_data import good_state_1
from city_data import good_city_1
from user_data import good_user_1, good_user_2
from place_data import good_place_1

''' Package import '''
import unittest
import json
import logging

class AppTestCase(unittest.TestCase):

	def setUp(self):
		db.connect()
		db.create_tables([User, State, City, Place, Review, ReviewUser, ReviewPlace], safe=True)
		logging.disable(logging.CRITICAL)
		self.app = app.test_client()

	def tearDown(self):
		db.drop_tables([User, State, City, Place, Review, ReviewUser, ReviewPlace])
		db.close()

	def test_create_user_review(self):
		''' Set base data '''
		rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
		self.assertEqual(rv.status_code, 201)
		data = json.loads(rv.data)
		self.assertEqual(data['id'], 1)
		rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_2))
		self.assertEqual(rv.status_code, 201)
		data = json.loads(rv.data)
		self.assertEqual(data['id'], 2)

		''' Test good reviews '''
		rv = self.app.post('/users/2/reviews', headers={'Content-Type': 'application/json'}, data=json.dumps(good_review_1))
		self.assertEqual(rv.status_code, 201)
		data = json.loads(rv.data)
		self.assertEqual(data['id'], 1)
		rv = self.app.post('/users/1/reviews', headers={'Content-Type': 'application/json'}, data=json.dumps(good_review_2))
		self.assertEqual(rv.status_code, 201)
		data = json.loads(rv.data)
		self.assertEqual(data['id'], 2)

		''' Test review for non-existent user '''
		rv = self.app.post('/users/404/reviews', headers={'Content-Type': 'application/json'}, data=json.dumps(good_review_1))
		self.assertEqual(rv.status_code, 404)

		''' Test missing message '''
		rv = self.app.post('/users/1/reviews', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_review_1))
		self.assertEqual(rv.status_code, 400)
		data = json.loads(rv.data)
		self.assertEqual(str(data['msg']), "Missing parameters")

		''' Test missing user_id '''
		rv = self.app.post('/users/1/reviews', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_review_2))
		self.assertEqual(rv.status_code, 400)
		data = json.loads(rv.data)
		self.assertEqual(str(data['msg']), "Missing parameters")

		''' Test bad data types for message '''
		rv = self.app.post('/users/1/reviews', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_review_3))
		self.assertEqual(rv.status_code, 400)
		data = json.loads(rv.data)
		self.assertEqual(str(data['msg']), "message is invalid")

		''' Test bad data types for user_id '''
		rv = self.app.post('/users/1/reviews', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_review_4))
		self.assertEqual(rv.status_code, 400)
		data = json.loads(rv.data)
		self.assertEqual(str(data['msg']), "user_id is invalid")

		''' Test bad data types for stars '''
		rv = self.app.post('/users/1/reviews', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_review_5))
		self.assertEqual(rv.status_code, 400)
		data = json.loads(rv.data)
		self.assertEqual(str(data['msg']), "stars is invalid")

	def test_get_user_reviews(self):
		''' Set base data '''
		rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
		self.assertEqual(rv.status_code, 201)
		data = json.loads(rv.data)
		self.assertEqual(data['id'], 1)
		rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_2))
		self.assertEqual(rv.status_code, 201)
		data = json.loads(rv.data)
		self.assertEqual(data['id'], 2)

		''' Test if user does not exist '''
		rv = self.app.get('/users/404/reviews')
		self.assertEqual(rv.status_code, 404)

		''' Test if no user reviews '''
		rv = self.app.get('/users/1/reviews')
		data = json.loads(rv.data)['data']
		self.assertEqual(len(data), 0)

		''' Test if 1 user review '''
		rv = self.app.post('/users/1/reviews', headers={'Content-Type': 'application/json'}, data=json.dumps(good_review_1))
		self.assertEqual(rv.status_code, 201)
		data = json.loads(rv.data)
		self.assertEqual(data['id'], 1)
		rv = self.app.get('/users/1/reviews')
		data = json.loads(rv.data)['data']
		self.assertEqual(len(data), 1)

	def test_get_user_review(self):
		''' Set base data '''
		rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
		self.assertEqual(rv.status_code, 201)
		rv = self.app.get('/users/1/reviews')
		data = json.loads(rv.data)['data']
		self.assertEqual(len(data), 0)
		rv = self.app.post('/users/1/reviews', headers={'Content-Type': 'application/json'}, data=json.dumps(good_review_1))
		self.assertEqual(rv.status_code, 201)
		data = json.loads(rv.data)
		self.assertEqual(data['id'], 1)

		''' Test if user does not exist '''
		rv = self.app.get('/users/404/reviews/1')
		self.assertEqual(rv.status_code, 404)

		''' Test if review does not exist '''
		rv = self.app.get('/users/1/reviews/404')
		self.assertEqual(rv.status_code, 404)

		''' Test if returns correct data '''
		rv = self.app.get('/users/1/reviews/1')
		self.assertEqual(rv.status_code, 200)
		data = json.loads(rv.data)
		self.assertEqual(data['message'],good_review_1['message'])
		self.assertEqual(data['stars'], good_review_1['stars'])

	def test_delete_user_review(self):
		''' Set base data '''
		rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
		self.assertEqual(rv.status_code, 201)
		rv = self.app.get('/users/1/reviews')
		data = json.loads(rv.data)['data']
		self.assertEqual(len(data), 0)
		rv = self.app.post('/users/1/reviews', headers={'Content-Type': 'application/json'}, data=json.dumps(good_review_1))
		self.assertEqual(rv.status_code, 201)
		data = json.loads(rv.data)
		self.assertEqual(data['id'], 1)

		''' Test if user does not exist '''
		rv = self.app.delete('/users/404/reviews/1')
		self.assertEqual(rv.status_code, 404)

		''' Test if review does not exist '''
		rv = self.app.delete('/users/1/reviews/404')
		self.assertEqual(rv.status_code, 404)

		''' Test if user review is deleted '''
		rv = self.app.get('/users/1/reviews/1')
		self.assertEqual(rv.status_code, 200)
		rv = self.app.delete('/users/1/reviews/1')
		self.assertEqual(rv.status_code, 200)
		rv = self.app.get('/users/1/reviews/1')
		self.assertEqual(rv.status_code, 404)

	def test_post_place_review(self):
		''' Set base data '''
		rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
		self.assertEqual(rv.status_code, 201)
		data = json.loads(rv.data)
		self.assertEqual(data['id'], 1)
		rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_2))
		self.assertEqual(rv.status_code, 201)
		data = json.loads(rv.data)
		self.assertEqual(data['id'], 2)
		rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_1))
		self.assertEqual(rv.status_code, 201)


		''' Test good reviews '''
		rv = self.app.post('/places/1/reviews', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_review_1))
		self.assertEqual(rv.status_code, 201)
		data = json.loads(rv.data)
		self.assertEqual(data['id'], 1)
		rv = self.app.post('/places/1/reviews', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_review_2))
		self.assertEqual(rv.status_code, 201)
		data = json.loads(rv.data)
		self.assertEqual(data['id'], 2)

		''' Test review for non-existent place '''
		rv = self.app.post('/places/404/reviews', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_review_1))
		self.assertEqual(rv.status_code, 404)

		''' Test missing message '''
		rv = self.app.post('/places/1/reviews', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_review_1))
		self.assertEqual(rv.status_code, 400)

		''' Test missing user_id '''
		rv = self.app.post('/places/1/reviews', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_review_2))
		self.assertEqual(rv.status_code, 400)

		''' Test bad data types for message '''
		rv = self.app.post('/places/1/reviews', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_review_3))
		self.assertEqual(rv.status_code, 400)

		''' Test bad data types for place_id '''
		rv = self.app.post('/places/1/reviews', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_review_4))
		self.assertEqual(rv.status_code, 400)

		''' Test bad data types for stars '''
		rv = self.app.post('/places/1/reviews', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_review_5))
		self.assertEqual(rv.status_code, 400)

	def test_get_place_reviews(self):
		''' Set base data '''
		rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
		self.assertEqual(rv.status_code, 201)
		data = json.loads(rv.data)
		self.assertEqual(data['id'], 1)
		rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_2))
		self.assertEqual(rv.status_code, 201)
		data = json.loads(rv.data)
		self.assertEqual(data['id'], 2)
		rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_1))
		self.assertEqual(rv.status_code, 201)

		''' Test if place does not exist '''
		rv = self.app.get('/places/404/reviews')
		self.assertEqual(rv.status_code, 404)

		''' Test if no place reviews '''
		rv = self.app.get('/places/1/reviews')
		data = json.loads(rv.data)['data']
		self.assertEqual(len(data), 0)

		''' Test if 1 place review '''
		rv = self.app.post('/places/1/reviews', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_review_1))
		self.assertEqual(rv.status_code, 201)
		data = json.loads(rv.data)
		self.assertEqual(data['id'], 1)
		rv = self.app.get('/places/1/reviews')
		data = json.loads(rv.data)['data']
		self.assertEqual(len(data), 1)

	def test_get_place_review(self):
		''' Set base data '''
		rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
		self.assertEqual(rv.status_code, 201)
		data = json.loads(rv.data)
		self.assertEqual(data['id'], 1)
		rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_2))
		self.assertEqual(rv.status_code, 201)
		data = json.loads(rv.data)
		self.assertEqual(data['id'], 2)
		rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_1))
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/places/1/reviews', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_review_1))
		self.assertEqual(rv.status_code, 201)

		''' Test if place does not exist '''
		rv = self.app.get('/places/404/reviews/1')
		self.assertEqual(rv.status_code, 404)

		''' Test if review does not exist '''
		rv = self.app.get('/places/1/reviews/404')
		self.assertEqual(rv.status_code, 404)

		''' Test if returns correct data '''
		rv = self.app.get('/places/1/reviews/1')
		self.assertEqual(rv.status_code, 200)
		data = json.loads(rv.data)
		self.assertEqual(data['message'],good_place_review_1['message'])
		self.assertEqual(data['stars'], good_place_review_1['stars'])

	def test_delete_place_review(self):
		''' Set base data '''
		rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
		self.assertEqual(rv.status_code, 201)
		data = json.loads(rv.data)
		self.assertEqual(data['id'], 1)
		rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_2))
		self.assertEqual(rv.status_code, 201)
		data = json.loads(rv.data)
		self.assertEqual(data['id'], 2)
		rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_1))
		self.assertEqual(rv.status_code, 201)
		rv = self.app.post('/places/1/reviews', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_review_1))
		self.assertEqual(rv.status_code, 201)

		''' Test if place does not exist '''
		rv = self.app.delete('/places/404/reviews/1')
		self.assertEqual(rv.status_code, 404)

		''' Test if review does not exist '''
		rv = self.app.delete('/places/1/reviews/404')
		self.assertEqual(rv.status_code, 404)

		''' Test if place review is deleted '''
		rv = self.app.get('/places/1/reviews/1')
		self.assertEqual(rv.status_code, 200)
		rv = self.app.delete('/places/1/reviews/1')
		self.assertEqual(rv.status_code, 200)
		rv = self.app.get('/places/1/reviews/1')
		self.assertEqual(rv.status_code, 404)

if __name__ == '__main__':
	unittest.main()

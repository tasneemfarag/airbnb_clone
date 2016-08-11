''' Import app and models '''
from app import app
from app.models.review_place import ReviewPlace
from app.models.review_user import ReviewUser
from app.models.review import Review
from app.models.user import User
from app.models.place import Place
from return_styles import ListStyle

''' Import packages '''
from flask_json import as_json, request
from datetime import datetime
from flask import abort
import json

@app.route('/users/<user_id>/reviews', methods=['GET'])
@as_json
def get_user_reviews(user_id):
	try:
		''' Test if user_id exists '''
		query = User.select().where(User.id == user_id)
		if not query.exists():
			raise LookupError('user_id')

		''' Get list of reviews for the user and return response '''
		reviews = Review.select(Review, ReviewUser).join(ReviewUser).where(ReviewUser.user == user_id)
		return ListStyle.list(reviews, request), 200
	except LookupError as e:
		abort(404)
	except Exception as e:
		print e.message
		res = {
			'code': 500,
			'msg': e.message
		}
		return res, 500


@app.route('/users/<user_id>/reviews', methods=['POST'])
@as_json
def create_user_reviews(user_id):
	data = request.json
	try:
		'''
		Data should include a user_id value that will be used to associate
		the review to the from user. The fromuserid is the user defined in
		in the Review model. The user_id from the route is used to associate
		the review to the user in the ReviewUser model.
		'''
		''' Test for required data '''
		if not data['user_id']:
			raise KeyError('user_id')
		elif not data['message']:
			raise KeyError('message')

		''' Test type of submitted data '''
		if not isinstance(data['user_id'], int):
			raise ValueError('user_id')
		elif not isinstance(data['message'], unicode):
			raise ValueError('message')
		elif 'stars' in data and not isinstance(data['stars'], int):
			raise ValueError('stars')

		''' Test if route user_id exists '''
		query = User.select().where(User.id == user_id)
		if not query.exists():
			raise LookupError('user_id')

		''' Test if data user_id exists '''
		query = User.select().where(User.id == data['user_id'])
		if not query.exists():
			raise LookupError('from_user_id')
		''' Create user Review and ReviewUser records'''
		new_review = Review(
			user_id = data['user_id'],
			message = data['message']
		)
		if 'stars' in data:
			new_review.stars = data['stars']
		new_review.save()
		new_user_review = ReviewUser.create(
			user = user_id,
			review = new_review.id
		)
		res = {}
		res['code'] = 201
		res['msg'] = 'Review saved successfully'
		res['id'] = new_review.id
		return res, 201
	except KeyError as e:
		res = {}
		res['code'] = 40000
		res['msg'] = 'Missing parameters'
		return res, 400
	except ValueError as e:
		res = {}
		res['code'] = 400
		res['msg'] = str(e.message) + ' is invalid'
		return res, 400
	except LookupError as e:
		abort(404)
	except Exception as e:
		res = {}
		res['code'] = 500
		res['msg'] = e.message
		print res
		return res, 500

@app.route('/users/<user_id>/reviews/<review_id>', methods=['GET'])
@as_json
def get_user_review(user_id, review_id):
	try:
		query = ReviewUser.select().where(ReviewUser.review == review_id, ReviewUser.user == user_id)
		if not query.exists():
			raise LookupError('Not found')
		query = Review.get(Review.id == review_id)
		data = query.to_dict()
		data['touserid'] = user_id
		return data, 200
	except LookupError as e:
		abort(404)
	except Exception as e:
		print e


@app.route('/users/<user_id>/reviews/<review_id>', methods=['DELETE'])
@as_json
def delete_user_review(user_id, review_id):
	try:
		query = ReviewUser.select().where(ReviewUser.review == review_id, ReviewUser.user == user_id)
		if not query.exists():
			raise LookupError('Not found')
		query = Review.select().where(Review.id == review_id)
		if not query.exists():
			raise LookupError('Not found')
		ReviewUser.delete().where(ReviewUser.review == review_id, ReviewUser.user == user_id).execute()
		Review.delete().where(Review.id == review_id).execute()
		res = {
			'code': 200,
			'msg': 'Review deleted successfully'
		}
		return res, 200
	except LookupError as e:
		abort(404)
	except Exception as e:
		print e

@app.route('/places/<place_id>/reviews', methods=['GET'])
@as_json
def get_place_reviews(place_id):
	try:
		''' Test if user_id exists '''
		query = Place.select().where(Place.id == place_id)
		if not query.exists():
			raise LookupError('place_id')

		''' Get list of reviews for the user '''
		reviews = Review.select(Review, ReviewPlace).join(ReviewPlace).where(ReviewPlace.place == place_id)
		return ListStyle.list(reviews, request), 200
	except LookupError as e:
		abort(404)
	except Exception as e:
		res = {
			'code': 500,
			'msg': e.message
		}
		return res, 500

@app.route('/places/<place_id>/reviews', methods=['POST'])
@as_json
def create_place_review(place_id):
	data = request.json
	try:
		''' Test for required data '''
		if not data['user_id']:
			raise KeyError('user_id')
		elif not data['message']:
			raise KeyError('message')

		''' Test type of submitted data '''
		if not isinstance(data['user_id'], int):
			raise ValueError('user_id')
		elif not isinstance(data['message'], unicode):
			raise ValueError('message')
		elif 'stars' in data and not isinstance(data['stars'], int):
			raise ValueError('stars')

		''' Test if route place_id exists '''
		query = Place.select().where(Place.id == place_id)
		if not query.exists():
			raise LookupError('place_id')

		''' Test if data user_id exists '''
		query = User.select().where(User.id == data['user_id'])
		if not query.exists():
			raise LookupError('user_id')

		''' Create user Review and ReviewUser records'''
		new_review = Review(
			user_id = data['user_id'],
			message = data['message']
		)
		if 'stars' in data:
			new_review.stars = data['stars']
		new_review.save()
		new_place_review = ReviewPlace.create(
			place = place_id,
			review = new_review.id
		)
		res = {}
		res['code'] = 201
		res['msg'] = 'Review saved successfully'
		res['id'] = new_review.id
		return res, 201
	except KeyError as e:
		res = {}
		res['code'] = 40000
		res['msg'] = 'Missing parameters'
		return res, 400
	except ValueError as e:
		res = {}
		res['code'] = 400
		res['msg'] = str(e.message) + ' is invalid'
		return res, 400
	except LookupError as e:
		abort(404)
	except Exception as e:
		res = {}
		res['code'] = 500
		res['msg'] = e.message
		return res, 500

@app.route('/places/<place_id>/reviews/<review_id>', methods=['GET'])
@as_json
def get_place_review(place_id, review_id):
	try:
		query = ReviewPlace.select().where(ReviewPlace.review == review_id, ReviewPlace.place == place_id)
		if not query.exists():
			raise LookupError('Not found')
		query = Review.get(Review.id == review_id)
		data = query.to_dict()
		data['toplaceid'] = place_id
		return data, 200
	except LookupError as e:
		abort(404)
	except Exception as e:
		print e

@app.route('/places/<place_id>/reviews/<review_id>', methods=['DELETE'])
@as_json
def delete_place_review(place_id, review_id):
	try:
		query = ReviewPlace.select().where(ReviewPlace.review == review_id, ReviewPlace.place == place_id)
		if not query.exists():
			raise LookupError('Not found')
		query = Review.select().where(Review.id == review_id)
		if not query.exists():
			raise LookupError('Not found')
		ReviewPlace.delete().where(ReviewPlace.review == review_id, ReviewPlace.place == place_id).execute()
		Review.delete().where(Review.id == review_id).execute()
		res = {
			'code': 200,
			'msg': 'Review deleted successfully'
		}
		return res, 200
	except LookupError as e:
		abort(404)
	except Exception as e:
		print e

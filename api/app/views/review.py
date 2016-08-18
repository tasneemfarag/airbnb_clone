''' Import app and models '''
from app import app
from app.models.review_place import ReviewPlace
from app.models.review_user import ReviewUser
from app.models.review import Review
from app.models.user import User
from app.models.place import Place
from return_styles import ListStyle
from index import type_test

''' Import packages '''
from flask_json import as_json, request
from datetime import datetime
from flask import abort
import json

@app.route('/users/<user_id>/reviews', methods=['GET'])
@as_json
def get_user_reviews(user_id):
	"""
	Get all user reviews
	List all user reviews in the database.
	---
	tags:
	    - Review
	parameters:
		-
			in: path
			name: user_id
			type: string
			required: True
			description: ID of the user
	responses:
	    200:
	        description: List of all user reviews
	        schema:
	            id: UserReviews
	            required:
	                - data
	                - paging
	            properties:
	                data:
	                    type: array
	                    description: user reviews array
	                    items:
	                        $ref: '#/definitions/get_user_review_get_UserReview'
	                paging:
	                    description: pagination
	                    schema:
	                        $ref: '#/definitions/get_amenities_get_Paging'
	"""
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
	"""
	Create a new user review
	Create a new review for the given user in the database
	---
	tags:
	    - Review
	parameters:
	    -
	        name: user_id
	        in: path
	        type: integer
	        required: True
	        description: id of the user being reviewed
	    -
	        name: user_id
	        in: form
	        type: integer
	        required: True
	        description: id of the user giving the review
	    -
	        name: message
	        in: form
	        type: string
	        required: True
	        description: the text of the review
	    -
	        name: stars
	        in: form
	        type: integer
	        description: number of stars given on the review
	responses:
	    201:
	        description: User review was created
	        schema:
	            $ref: '#/definitions/create_amenity_post_post_success'
	    400:
	        description: Issue with user review request
	    404:
	        description: A user was not found
	    500:
	        description: The request was not able to be processed
	"""
	data = {}
	for key in request.form.keys():
		for value in request.form.getlist(key):
			data[key] = value
	try:
		''' Test for required data '''
		if not data['user_id']:
			raise KeyError('user_id')
		elif not data['message']:
			raise KeyError('message')

		''' Test type of submitted data '''
		if not type_test(data['user_id'], int):
			raise ValueError('user_id')
		elif not type_test(data['message'], 'string'):
			raise ValueError('message')
		elif 'stars' in data and not type_test(data['stars'], int):
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
	"""
	Get the given user view
	Returns the given user review in the database.
	---
	tags:
		- Review
	parameters:
		-
			in: path
			name: user_id
			type: string
			required: True
			description: ID of the user
		-
			in: path
			name: review_id
			type: string
			required: True
			description: ID of the review
	responses:
	    200:
	        description: User review returned successfully
	        schema:
	            id: UserReview
	            required:
	                - fromuserid
	                - message
	                - touserid
	                - id
	                - created_at
	                - updated_at
	            properties:
	                message:
	                    type: string
	                    description: message of the review
	                    default: 'Super awesome!'
	                stars:
	                    type: integer
	                    description: number of stars given on review
	                    default: 5
	                fromuserid:
	                    type: integer
	                    description: id of the user giving the review
	                    default: 1
	                touserid:
	                    type: integer
	                    description: id of the user receiving the review
	                    default: 2
	                toplaceid:
	                    type: integer
	                    description: id of the place receiving the review
	                    default: None
	                id:
	                    type: integer
	                    description: id of the review
	                    default: 1
	                created_at:
	                    type: datetime string
	                    description: date and time the review was created in the database
	                    default: '2016-08-11 20:30:38'
	                updated_at:
	                    type: datetime string
	                    description: date and time the review was updated in the database
	                    default: '2016-08-11 20:30:38'
	    404:
	        description: Review or a user was not found
	    500:
	        description: Request could not be processed
    """
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
	"""
    Delete the given user review
    Deletes the given user review in the database.
    ---
    tags:
        - Review
    parameters:
        -
            in: path
            name: user_id
            type: integer
            required: True
            description: ID of the user reviewed
		-
            in: path
            name: review_id
            type: integer
            required: True
            description: ID of the review
    responses:
        200:
            description: User review deleted successfully
            schema:
                $ref: '#/definitions/delete_amenity_delete_delete_200'
        404:
            description: A user was not found
        500:
            description: Request could not be processed
    """
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
	"""
	Get all place reviews
	List all place reviews in the database.
	---
	tags:
	    - Review
	parameters:
		-
			in: path
			name: place_id
			type: string
			required: True
			description: ID of the place
	responses:
	    200:
	        description: List of all place reviews
	        schema:
	            id: PlaceReviews
	            required:
	                - data
	                - paging
	            properties:
	                data:
	                    type: array
	                    description: place reviews array
	                    items:
	                        $ref: '#/definitions/get_place_review_get_PlaceReview'
	                paging:
	                    description: pagination
	                    schema:
	                        $ref: '#/definitions/get_amenities_get_Paging'
	"""
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
	"""
	Create a new place review
	Create a new review for the given place in the database
	---
	tags:
	    - Review
	parameters:
	    -
	        name: place_id
	        in: path
	        type: integer
	        required: True
	        description: id of the place being reviewed
	    -
	        name: user_id
	        in: form
	        type: integer
	        required: True
	        description: id of the user giving the review
	    -
	        name: message
	        in: form
	        type: string
	        required: True
	        description: the text of the review
	    -
	        name: stars
	        in: form
	        type: integer
	        description: number of stars given on the review
	responses:
	    201:
	        description: Place review was created
	        schema:
	            $ref: '#/definitions/create_amenity_post_post_success'
	    400:
	        description: Issue with place review request
	    404:
	        description: Place or user was not found
	    500:
	        description: The request was not able to be processed
	"""
	data = {}
	for key in request.form.keys():
		for value in request.form.getlist(key):
			data[key] = value
	try:
		''' Test for required data '''
		if not data['user_id']:
			raise KeyError('user_id')
		elif not data['message']:
			raise KeyError('message')

		''' Test type of submitted data '''
		if not type_test(data['user_id'], int):
			raise ValueError('user_id')
		elif not type_test(data['message'], 'string'):
			raise ValueError('message')
		elif 'stars' in data and not type_test(data['stars'], int):
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
	"""
	Get the given place review
	Returns the given place review in the database.
	---
	tags:
		- Review
	parameters:
		-
			in: path
			name: place_id
			type: string
			required: True
			description: ID of the place
		-
			in: path
			name: review_id
			type: string
			required: True
			description: ID of the review
	responses:
	    200:
	        description: Place review returned successfully
	        schema:
	            id: PlaceReview
	            required:
	                - fromuserid
	                - message
	                - toplaceid
	                - id
	                - created_at
	                - updated_at
	            properties:
	                message:
	                    type: string
	                    description: message of the review
	                    default: 'Super awesome!'
	                stars:
	                    type: integer
	                    description: number of stars given on review
	                    default: 5
	                fromuserid:
	                    type: integer
	                    description: id of the user giving the review
	                    default: 1
	                touserid:
	                    type: integer
	                    description: id of the user receiving the review
	                    default: None
	                toplaceid:
	                    type: integer
	                    description: id of the place receiving the review
	                    default: 1
	                id:
	                    type: integer
	                    description: id of the review
	                    default: 1
	                created_at:
	                    type: datetime string
	                    description: date and time the review was created in the database
	                    default: '2016-08-11 20:30:38'
	                updated_at:
	                    type: datetime string
	                    description: date and time the review was updated in the database
	                    default: '2016-08-11 20:30:38'
	    404:
	        description: Review, user or place was not found
	    500:
	        description: Request could not be processed
    """
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
	"""
    Delete the given place review
    Deletes the given place review in the database.
    ---
    tags:
        - Review
    parameters:
        -
            in: path
            name: place_id
            type: integer
            required: True
            description: ID of the place reviewed
		-
            in: path
            name: review_id
            type: integer
            required: True
            description: ID of the review
    responses:
        200:
            description: Place review deleted successfully
            schema:
                $ref: '#/definitions/delete_amenity_delete_delete_200'
        404:
            description: Place or user was not found
        500:
            description: Request could not be processed
    """
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

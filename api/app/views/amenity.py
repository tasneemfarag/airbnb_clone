from app.models.amenity import Amenity
from app.models.place import Place
from app.models.place_amenity import PlaceAmenities
from flask_json import as_json, request
from flask import abort
from app import app
from datetime import datetime
import json
from peewee import OperationalError

@app.route('/amenities', methods=['GET'])
@as_json
def get_amenities():
    ''' Returns all amenities in a list named result '''
    amenities = []
    data = Amenity.select()
    for row in data:
        amenities.append(row.to_hash())
    return {"result": amenities}, 200

@app.route('/amenities', methods=['POST'])
@as_json
def create_amenity():
    ''' Creates a new amenity '''
    data = request.get_json()
    try:
        if data['name'] and not isinstance(data['name'], unicode):
            raise OperationalError("Amenity 'name' must be a string value")
        new = Amenity.create(
            name = data['name']
        )
        res = {}
        res['code'] = 201
        res['id'] = new.id
        res['msg'] = "Amenity was created successfully"
        return res, 201
    except KeyError as error:
        response = {}
        response['code'] = 400
        response['msg'] = str(error.message) + ' is missing'
        return response, 400
    except Exception as error:
        if type(error).__name__ == 'OperationalError':
            response = {}
            response['code'] = 400
            response['msg'] = error.message
            return response, 400
        print error
        print type(error)
        print type(error).__name__
        response = {}
        response['code'] = 10003
        response['msg'] = "Name already exists"
        return response, 500

@app.route('/amenities/<amenity_id>', methods=['GET'])
@as_json
def get_amenity(amenity_id):
    ''' Gets the details of the given amenity '''
    try:
        amenity = Amenity.get(Amenity.id == amenity_id)
        return amenity.to_hash(), 200
    except Exception as error:
        if "Instance matching query does not exist" in error.message:
            abort(404)

@app.route('/amenities/<amenity_id>', methods=['DELETE'])
@as_json
def delete_amenity(amenity_id):
    ''' Deletes the given amenity '''
    try:
        amenity = Amenity.delete().where(Amenity.id == amenity_id)
        amenity.execute()
        res = {}
        res['code'] = 201
        res['msg'] = "Amenity was deleted successfully"
        return res, 201
    except Exception as error:
        if "Instance matching query does not exist" in error.message:
            abort(404)

@app.route('/places/<place_id>/amenities', methods=['GET'])
@as_json
def get_place_amenities(place_id):
    ''' Gets all amenities for the given place '''
    try:
        query = Place.select().where(Place.id == place_id)
        if not query.exists():
            raise LookupError('place_id')
        amenities = []
        data = Amenity.select().join(PlaceAmenities).where(PlaceAmenities.place == place_id)
        for row in data:
            amenities.append(row.to_hash())
        return {"result": amenities}, 200
    except LookupError as e:
        abort(404)
    except Exception as error:
        if "Instance matching query does not exist" in error.message:
            abort(404)

@app.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
@as_json
def post_place_amenity(place_id, amenity_id):
    try:
        ''' Check if place_id is valid '''
        query = Place.select().where(Place.id == place_id)
        if not query.exists():
            raise LookupError('place_id')

        ''' Check if amenity_id is valid '''
        query = Amenity.select().where(Amenity.id == amenity_id)
        if not query.exists():
            raise LookupError('amenity_id')

        ''' Check if amenity is already added for place '''
        query = PlaceAmenities.select().where(PlaceAmenities.amenity == amenity_id, PlaceAmenities.place == place_id)
        if query.exists():
            raise ValueError('Amenity is already set for the given place')

        ''' Add amenity for place '''
        new = PlaceAmenities.create(
            place = place_id,
            amenity = amenity_id
        )
        res = {
            'code': 201,
            'msg': 'Amenity added successfully for the given place'
        }
        return res, 201
    except LookupError as e:
        abort(404)
    except ValueError as e:
        res = {
            'code': 400,
            'msg': e.message
        }
        return res, res['code']
    except Exception as e:
        res = {
            'code': 500,
            'msg': e.message
        }
        return res, 500

@app.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
@as_json
def delete_place_amenity(place_id, amenity_id):
    try:
        ''' Check if place_id is valid '''
        query = Place.select().where(Place.id == place_id)
        if not query.exists():
            raise LookupError('place_id')

        ''' Check if amenity_id is valid '''
        query = Amenity.select().where(Amenity.id == amenity_id)
        if not query.exists():
            raise LookupError('amenity_id')

        ''' Check if amenity is already added for place '''
        query = PlaceAmenities.select().where(PlaceAmenities.amenity == amenity_id, PlaceAmenities.place == place_id)
        if not query.exists():
            raise LookupError('amenity_id, place_id')

        ''' Add amenity for place '''
        delete = PlaceAmenities.delete().where(
            PlaceAmenities.amenity == amenity_id,
            PlaceAmenities.place == place_id
        )
        delete.execute()
        res = {
            'code': 200,
            'msg': 'Amenity deleted successfully for the given place'
        }
        return res, 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        res = {
            'code': 500,
            'msg': e.message
        }
        return res, 500

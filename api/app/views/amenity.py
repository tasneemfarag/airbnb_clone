''' Import app and models '''
from app import app
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.place_amenity import PlaceAmenities

''' Import packages '''
from flask_json import as_json, request
from flask import abort
from datetime import datetime
from peewee import OperationalError
import json

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
        ''' Check if name for amenity was given '''
        if not 'name' in data:
            raise KeyError("'name'")

        ''' Check if name is a string '''
        if not isinstance(data['name'], unicode):
            raise TypeError("Amenity 'name' must be a string value")

        ''' Check if amenity already exists '''
        query = Amenity.select().where(Amenity.name == data['name'])
        if query.exists():
            raise ValueError('Amenity already exists')

        ''' Create new amenity '''
        new = Amenity.create(
            name = data['name']
        )
        res = {}
        res['code'] = 201
        res['id'] = new.id
        res['msg'] = "Amenity was created successfully"
        return res, 201
    except KeyError as e:
        res = {}
        res['code'] = 40000
        res['msg'] = 'Missing parameters'
        return res, 400
    except TypeError as e:
        res = {}
        res['code'] = 400
        res['msg'] = e.message
        return res, 400
    except ValueError as e:
        res = {}
        res['code'] = 10003
        res['msg'] = e.message
        return res, 409
    except Exception as e:
        abort(500)

@app.route('/amenities/<amenity_id>', methods=['GET'])
@as_json
def get_amenity(amenity_id):
    ''' Gets the details of the given amenity '''
    try:
        ''' Check if amenity exists '''
        query = Amenity.select().where(Amenity.id == amenity_id)
        if not query.exists():
            raise LookupError('amenity_id')

        ''' Return amenity data '''
        amenity = Amenity.get(Amenity.id == amenity_id)
        return amenity.to_hash(), 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        abort(500)

@app.route('/amenities/<amenity_id>', methods=['DELETE'])
@as_json
def delete_amenity(amenity_id):
    ''' Deletes the given amenity '''
    try:
        ''' Check if amenity exists '''
        query = Amenity.select().where(Amenity.id == amenity_id)
        if not query.exists():
            raise LookupError('amenity_id')

        ''' Delete the amenity '''
        amenity = Amenity.delete().where(Amenity.id == amenity_id)
        amenity.execute()
        res = {}
        res['code'] = 200
        res['msg'] = "Amenity was deleted successfully"
        return res, 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        abort(500)

@app.route('/places/<place_id>/amenities', methods=['GET'])
@as_json
def get_place_amenities(place_id):
    ''' Gets all amenities for the given place '''
    try:
        ''' Check if the place exists '''
        query = Place.select().where(Place.id == place_id)
        if not query.exists():
            raise LookupError('place_id')

        ''' Return amenities for the given place '''
        amenities = []
        data = Amenity.select().join(PlaceAmenities).where(PlaceAmenities.place == place_id)
        for row in data:
            amenities.append(row.to_hash())
        return {"result": amenities}, 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        abort(500)

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
        res = {}
        res['code'] = 400
        res['msg'] = e.message
        return res, res['code']
    except Exception as e:
        abort(500)

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
        res = {}
        res['code'] = 200
        res['msg'] = 'Amenity deleted successfully for the given place'
        return res, 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        abort(500)

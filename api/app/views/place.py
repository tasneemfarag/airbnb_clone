from app.models.place import Place
from app.models.city import City
from app.models.state import State
from flask_json import as_json, request
from app import app
from datetime import datetime
from flask import abort
import json

@app.route('/places', methods=['GET'])
@as_json
def get_places():
    ''' Returns all places in a list named result '''
    places = []
    data = Place.select()
    for row in data:
        places.append(row.to_hash())
    return {"result": places}, 200

@app.route('/places', methods=['POST'])
@as_json
def create_place():
    try:
        ''' Creates a new place '''
        data = request.get_json()
        new = Place(
            owner = data['owner_id'],
            name = data['name'],
            city = data['city_id']
        )
        if data['description']:
            new.description = data['description']
        if data['number_rooms']:
            new.number_rooms = data['number_rooms']
        if data['number_bathrooms']:
            new.number_bathrooms = data['number_bathrooms']
        if data['max_guest']:
            new.max_guest = data['max_guest']
        if data['price_by_night']:
            new.price_by_night = data['price_by_night']
        if data['latitude']:
            new.latitude = data['latitude']
        if data['longitude']:
            new.longitude = data['longitude']
        new.save()
        res = {}
        res['code'] = 201
        res['id'] = new.id
        res['msg'] = "Place was created successfully"
        return res, 201
    except KeyError as e:
        res = {}
        res['code'] = 400
        res['msg'] = str(e.message) + " is missing"
        return res, 400
    except ValueError as e:
        res = {}
        res['code'] = 400
        res['msg'] = e.message
        return res, 400
    except Exception as e:
        res = {}
        res['code'] = 500
        res['msg'] = e.message
        print type(e)
        print res
        return res, 500

@app.route('/places/<place_id>', methods=['GET'])
@as_json
def get_place(place_id):
    ''' Gets a given place '''
    try:
        place = Place.get(Place.id == place_id)
        return place.to_hash(), 200
    except Exception as error:
        if "Instance matching query does not exist" in error.message:
            abort(404)

@app.route('/places/<place_id>', methods=['PUT'])
@as_json
def update_place(place_id):
    ''' Updates a given place '''
    try:
        data = json.loads(request.data)
        place = Place.get(Place.id == place_id)
        for key in data:
            if key == 'owner_id':
                raise Exception('Owner cannot be changed')
            elif key == 'city_id':
                raise Exception('City cannot be changed')
            elif key == 'name':
                place.name = data[key]
            elif key == 'description':
                place.description = data[key]
            elif key == 'number_rooms':
                place.number_rooms = data[key]
            elif key == 'number_bathrooms':
                place.number_bathrooms = data[key]
            elif key == 'max_guest':
                place.max_guest = data[key]
            elif key == 'price_by_night':
                place.price_by_night = data[key]
            elif key == 'latitude':
                place.latitude = data[key]
            elif key == 'longitude':
                place.longitude = data[key]
        place.save()
        res = {}
        res['code'] = 200
        res['msg'] = "Place was updated successfully"
        return res, 200
    except Exception as error:
        if "Instance matching query does not exist" in error.message:
            abort(404)
        else:
            res = {}
            res['code'] = 403
            res['msg'] = str(error)
            return res, 403

@app.route('/places/<place_id>', methods=['DELETE'])
@as_json
def delete_place(place_id):
    ''' Deletes the given place '''
    try:
        delete_place = Place.delete().where(Place.id == place_id)
        delete_place.execute()
        response = {}
        response['code'] = 200
        response['msg'] = "Place was deleted"
        return response, 200
    except Exception as error:
        if "Instance matching query does not exist" in error.message:
            abort(404)

@app.route('/states/<state_id>/cities/<city_id>/places', methods=['GET'])
@as_json
def get_places_by_city(state_id, city_id):
    ''' Gets all places in a city '''
    try:
        city = City.get(City.id == city_id, City.state == state_id)
        places = []
        data = Place.select().where(Place.city == city.id)
        for row in data:
            places.append(row.to_hash())
        return {"result": places}, 200
    except Exception as error:
        if "Instance matching query does not exist" in error.message:
            abort(404)

@app.route('/states/<state_id>/cities/<city_id>/places', methods=['POST'])
@as_json
def create_place_by_city(state_id, city_id):
    ''' Creates a new place in a city '''
    try:
        data = request.get_json()
        city = City.get(City.id == city_id, City.state == state_id)
        new = Place(
            owner = data['owner_id'],
            name = data['name'],
            city = city.id
        )
        if data['description']:
            new.description = data['description']
        if data['number_rooms']:
            new.number_rooms = data['number_rooms']
        if data['number_bathrooms']:
            new.number_bathrooms = data['number_bathrooms']
        if data['max_guest']:
            new.max_guest = data['max_guest']
        if data['price_by_night']:
            new.price_by_night = data['price_by_night']
        if data['latitude']:
            new.latitude = data['latitude']
        if data['longitude']:
            new.longitude = data['longitude']
        new.save()
        res = {}
        res['code'] = 201
        res['id'] = new.id
        res['msg'] = "Place was created successfully"
        return res, 201
    except KeyError as e:
        res = {}
        res['code'] = 400
        res['msg'] = str(e.message) + " is missing"
        return res, 400
    except ValueError as e:
        res = {}
        res['code'] = 400
        res['msg'] = e.message
        return res, 400
    except Exception as e:
        res = {}
        res['code'] = 500
        res['msg'] = e.message
        print type(e)
        print res
        return res, 500

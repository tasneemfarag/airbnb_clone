''' Import app and models '''
from app import app
from app.models.place import Place
from app.models.city import City
from app.models.state import State
from app.models.user import User

''' Import packages '''
from flask_json import as_json, request
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
    data = json.loads(request.data)
    try:
        ''' Check for required keys '''
        if not 'owner_id' in data:
            raise KeyError('owner_id')
        if not 'name' in data:
            raise KeyError('name')
        if not 'city_id' in data:
            raise KeyError('city_id')

        ''' Check required key value data types '''
        if not isinstance(data['owner_id'], int):
            raise TypeError('owner_id is not an integer')
        if not isinstance(data['name'], unicode):
            raise TypeError('name is not a string')
        if not isinstance(data['city_id'], int):
            raise TypeError('city_id is not an integer')

        ''' Check optional key value data types '''
        if 'description' in data and not isinstance(data['description'], unicode):
            raise TypeError('description is not a string')
        if 'number_rooms' in data and not isinstance(data['number_rooms'], int):
            raise TypeError('number_rooms is not an integer')
        if 'number_bathrooms' in data and not isinstance(data['number_bathrooms'], int):
            raise TypeError('number_bathrooms is not an integer')
        if 'max_guest' in data and not isinstance(data['max_guest'], int):
            raise TypeError('max_guest is not an integer')
        if 'price_by_night' in data and not isinstance(data['price_by_night'], int):
            raise TypeError('price_by_night is not an integer')
        if 'latitude' in data and not isinstance(data['latitude'], float):
            raise TypeError('latitude is not a float')
        if 'longitude' in data and not isinstance(data['longitude'], float):
            raise TypeError('longitude is not a float')

        ''' Check if city_id exists '''
        query = City.select().where(City.id == data['city_id'])
        if not query.exists():
            raise LookupError('city_id')

        ''' Check if owner_id exists '''
        query = User.select().where(User.id == data['owner_id'])
        if not query.exists():
            raise LookupError('owner_id')


        ''' Creates a new place '''
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
    except TypeError as e:
        res = {}
        res['code'] = 400
        res['msg'] = e.message
        return res, 400
    except LookupError as e:
        abort(404)
    except Exception as e:
        abort(500)

@app.route('/places/<place_id>', methods=['GET'])
@as_json
def get_place(place_id):
    ''' Gets a given place '''
    try:
        ''' Check if place_id exists '''
        query = Place.select().where(Place.id == place_id)
        if not query.exists():
            raise LookupError('place_id')

        ''' Return place data '''
        place = Place.get(Place.id == place_id)
        return place.to_hash(), 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        abort(500)

@app.route('/places/<place_id>', methods=['PUT'])
@as_json
def update_place(place_id):
    ''' Updates a given place '''
    try:
        data = json.loads(request.data)

        ''' Check if place_id exists '''
        query = Place.select().where(Place.id == place_id)
        if not query.exists():
            raise LookupError('place_id')

        ''' Check that no request to change protected values '''
        if 'owner_id' in data:
            raise ValueError('Owner cannot be changed')
        if 'city_id' in data:
            raise ValueError('City cannot be changed')

        ''' Check for valid data types '''
        if 'name' in data and not isinstance(data['name'], unicode):
            raise TypeError('name is not a string')
        if 'description' in data and not isinstance(data['description'], unicode):
            raise TypeError('description is not a string')
        if 'number_rooms' in data and not isinstance(data['number_rooms'], int):
            raise TypeError('number_rooms is not an integer')
        if 'number_bathrooms' in data and not isinstance(data['number_bathrooms'], int):
            raise TypeError('number_bathrooms is not an integer')
        if 'max_guest' in data and not isinstance(data['max_guest'], int):
            raise TypeError('max_guest is not an integer')
        if 'price_by_night' in data and not isinstance(data['price_by_night'], int):
            raise TypeError('price_by_night is not an integer')
        if 'latitude' in data and not isinstance(data['latitude'], float):
            raise TypeError('latitude is not a float')
        if 'longitude' in data and not isinstance(data['longitude'], float):
            raise TypeError('longitude is not a float')

        place = Place.get(Place.id == place_id)
        for key in data:
            if key == 'name':
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
    except ValueError as e:
        res = {}
        res['code'] = 403
        res['msg'] = e.message
        return res, 403
    except LookupError as e:
        abort(404)
    except TypeError as e:
        res = {}
        res['code'] = 400
        res['msg'] = e.message
        return res, 400
    except Exception as error:
        abort(500)

@app.route('/places/<place_id>', methods=['DELETE'])
@as_json
def delete_place(place_id):
    ''' Deletes the given place '''
    try:
        ''' Check if place_id exists '''
        query = Place.select().where(Place.id == place_id)
        if not query.exists():
            raise LookupError('place_id')

        ''' Delete the given place '''
        delete_place = Place.delete().where(Place.id == place_id)
        delete_place.execute()
        response = {}
        response['code'] = 200
        response['msg'] = "Place was deleted"
        return response, 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        abort(505)

@app.route('/states/<state_id>/cities/<city_id>/places', methods=['GET'])
@as_json
def get_places_by_city(state_id, city_id):
    ''' Gets all places in a city '''
    try:
        ''' Check if the state_id exists '''
        query = State.select().where(State.id == state_id)
        if not query.exists():
            raise LookupError('state_id')

        ''' Check if the city_id exists '''
        query = City.select().where(City.id == city_id)
        if not query.exists():
            raise LookupError('city_id')

        ''' Check if the city_id is associated to the state_id '''
        city = City.get(City.id == city_id)
        query = State.select().where(State.id == city.state, State.id == state_id)
        if not query.exists():
            raise LookupError('city_id, state_id')

        ''' Return all places in the given city '''
        places = []
        data = Place.select().where(Place.city == city.id)
        for row in data:
            places.append(row.to_hash())
        return {"result": places}, 200
    except LookupError as e:
        abort(404)
    except Exception as error:
        abort(500)

@app.route('/states/<state_id>/cities/<city_id>/places', methods=['POST'])
@as_json
def create_place_by_city(state_id, city_id):
    ''' Creates a new place in a city '''
    try:
        data = json.loads(request.data)

        ''' Check for required keys '''
        if not 'owner_id' in data:
            raise KeyError('owner_id')
        if not 'name' in data:
            raise KeyError('name')

        ''' Check required key value data types '''
        if not isinstance(data['owner_id'], int):
            raise TypeError('owner_id is not an integer')
        if not isinstance(data['name'], unicode):
            raise TypeError('name is not a string')

        ''' Check optional key value data types '''
        if 'description' in data and not isinstance(data['description'], unicode):
            raise TypeError('description is not a string')
        if 'number_rooms' in data and not isinstance(data['number_rooms'], int):
            raise TypeError('number_rooms is not an integer')
        if 'number_bathrooms' in data and not isinstance(data['number_bathrooms'], int):
            raise TypeError('number_bathrooms is not an integer')
        if 'max_guest' in data and not isinstance(data['max_guest'], int):
            raise TypeError('max_guest is not an integer')
        if 'price_by_night' in data and not isinstance(data['price_by_night'], int):
            raise TypeError('price_by_night is not an integer')
        if 'latitude' in data and not isinstance(data['latitude'], float):
            raise TypeError('latitude is not a float')
        if 'longitude' in data and not isinstance(data['longitude'], float):
            raise TypeError('longitude is not a float')

        ''' Check if the state_id exists '''
        query = State.select().where(State.id == state_id)
        if not query.exists():
            raise LookupError('state_id')

        ''' Check if the city_id exists '''
        query = City.select().where(City.id == city_id)
        if not query.exists():
            raise LookupError('city_id')

        ''' Check if the city_id is associated to the state_id '''
        city = City.get(City.id == city_id)
        query = State.select().where(State.id == city.state, State.id == state_id)
        if not query.exists():
            raise LookupError('city_id, state_id')

        ''' Check if the owner_id exists '''
        query = User.select().where(User.id == data['owner_id'])
        if not query.exists():
            raise LookupError('owner_id')
        
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
    except LookupError as e:
        abort(404)
    except TypeError as e:
        res = {}
        res['code'] = 400
        res['msg'] = e.message
        return res, 400
    except Exception as e:
        print e.message
        abort(500)

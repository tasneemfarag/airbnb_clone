''' Import app and models '''
from app import app
from app.models.city import City
from app.models.city import State

''' Import packages '''
from flask_json import as_json, request
from flask import abort
from datetime import datetime
import json

@app.route('/states/<state_id>/cities', methods=['GET'])
@as_json
def get_cities(state_id):
    ''' Returns all cities in a given state '''
    try:
        ''' Check if state exists '''
        query = State.select().where(State.id == state_id)
        if not query.exists():
            raise LookupError('state')

        ''' Return list of cities in given state '''
        cities = []
        data = City.select().where(City.state == state_id)
        for row in data:
            cities.append(row.to_dict())
        return {"result": cities}, 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        abort(500)

@app.route('/states/<state_id>/cities', methods=['POST'])
@as_json
def create_city(state_id):
    ''' Creates a new city in a given state '''
    data = json.loads(request.data)
    try:
        ''' Check if state exists '''
        query = State.select().where(State.id == state_id)
        if not query.exists():
            raise LookupError('state_id')

        ''' Check if 'name' key in data '''
        if not 'name' in data:
            raise KeyError('name')

        ''' Check if 'name' value is a string '''
        if not isinstance(data['name'], unicode):
            raise TypeError("'name' value is not a string")

        ''' Check if city already exists '''
        query = City.select().where(City.name == data['name'])
        if query.exists():
            raise ValueError('City already exists')

        ''' Create new city in given state '''
        new = City.create(
            name = data['name'],
            state_id = state_id
        )
        res = {}
        res['code'] = 201
        res['id'] = int(new.id)
        res['msg'] = "City was created successfully"
        return res, 201
    except KeyError as e:
        res = {}
        res['code'] = 40000
        res['msg'] = 'Missing parameters'
        return res, 400
    except LookupError as e:
        abort(404)
    except TypeError as e:
        res = {}
        res['code'] = 400
        res['msg'] = e.message
        return res, 400
    except ValueError as e:
        res = {}
        res['code'] = 10002
        res['msg'] = e.message
        return res, 409
    except Exception as e:
        abort(500)

@app.route('/states/<state_id>/cities/<city_id>', methods=['GET'])
@as_json
def get_city(state_id, city_id):
    ''' Returns details for a given city '''
    try:
        ''' Check if state exists '''
        query = State.select().where(State.id == state_id)
        if not query.exists():
            raise LookupError('state_id')

        ''' Check if city exists '''
        query = City.select().where(City.id == city_id)
        if not query.exists():
            raise LookupError('city_id')

        ''' Return city data '''
        city = City.get(City.id == city_id, City.state == state_id)
        return city.to_dict(), 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        abort(500)

@app.route('/states/<state_id>/cities/<city_id>', methods=['DELETE'])
@as_json
def delete_city(state_id, city_id):
    ''' Deletes the given city '''
    try:
        ''' Check if state exists '''
        query = State.select().where(State.id == state_id)
        if not query.exists():
            raise LookupError('state_id')

        ''' Check if city exists '''
        query = City.select().where(City.id == city_id)
        if not query.exists():
            raise LookupError('city_id')

        ''' Delete the city from the given state '''
        delete_city = City.delete().where(City.id == city_id, City.state == state_id)
        delete_city.execute()
        response = {}
        response['code'] = 200
        response['msg'] = "City account was deleted"
        return response, 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        abort(500)

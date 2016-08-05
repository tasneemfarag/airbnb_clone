from app.models.city import City
from app.models.city import State
from flask_json import as_json, request
from flask import abort
from app import app
from datetime import datetime
from peewee import OperationalError
import json

@app.route('/states/<state_id>/cities', methods=['GET'])
@as_json
def get_cities(state_id):
    ''' Returns all cities in a given state '''
    try:
        cities = []
        data = City.select().where(City.state == state_id)
        for row in data:
            cities.append(row.to_hash())
        return {"result": cities}, 200
    except Exception as error:
        if "Instance matching query does not exist" in error.message:
            abort(404)

@app.route('/states/<state_id>/cities', methods=['POST'])
@as_json
def create_city(state_id):
    ''' Creates a new city in a given state '''
    data = json.loads(request.data)
    try:
        if data['name'] and not isinstance(data['name'], unicode):
            raise OperationalError("City 'name' must be a string value")
        new = City.create(
            name = data['name'],
            state_id = state_id
        )
        res = {}
        res['code'] = 201
        res['id'] = new.id
        res['msg'] = "City was created successfully"
        return res, 201
    except KeyError as error:
        response = {}
        response['code'] = 400
        response['msg'] = str(error.message) + ' is missing'
        return response, 400
    except Exception as error:
        if type(error).__name__ == 'IntegrityError':
            abort(404)
        elif type(error).__name__ == 'OperationalError':
            response = {}
            response['code'] = 400
            response['msg'] = error.message
            return response, 400
        else:
            print error
            print type(error)
            print type(error).__name__
            response = {}
            response['code'] = 10002
            response['msg'] = "City already exists in this state"
            return response, 500

@app.route('/states/<state_id>/cities/<city_id>', methods=['GET'])
@as_json
def get_city(state_id, city_id):
    ''' Returns details for a given city '''
    try:
        city = City.get(City.id == city_id, City.state == state_id)
        return city.to_hash(), 200
    except Exception as error:
        if "Instance matching query does not exist" in error.message:
            abort(404)

@app.route('/states/<state_id>/cities/<city_id>', methods=['DELETE'])
@as_json
def delete_city(state_id, city_id):
    ''' Deletes the given city '''
    try:
        delete_city = City.delete().where(City.id == city_id, City.state == state_id)
        delete_city.execute()
        response = {}
        response['code'] = 200
        response['msg'] = "City account was deleted"
        return response, 200
    except Exception as error:
        if "Instance matching query does not exist" in error.message:
            abort(404)

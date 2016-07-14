from app.models.city import City
from app.models.city import State
from flask_json import as_json, request
from app import app
from datetime import datetime
import json

@app.route('/states/<state_id>/cities', methods=['GET'])
@as_json
def get_cities(state_id):
    cities = []
    data = City.select().where(City.state == state_id)
    for row in data:
        cities.append(row.to_hash())
    return {"result": cities}, 200

@app.route('/states/<state_id>/cities', methods=['POST'])
@as_json
def create_city(state_id):
    data = request.get_json()
    try:
        new = City.create(
            name = data['name'],
            state_id = state_id
        )
        res = {}
        res['code'] = 201
        res['msg'] = "City was created successfully"
        return res, 201
    except Exception as e:
        print str(e)
        response = {}
        response['code'] = 10002
        response['msg'] = "City already exists in this state"
        return response, 409

@app.route('/states/<state_id>/cities/<city_id>', methods=['GET'])
@as_json
def get_city(state_id, city_id):
    city = City.get(City.id == city_id, City.state == state_id)
    return city.to_hash(), 200

@app.route('/states/<state_id>/cities/<city_id>', methods=['DELETE'])
@as_json
def delete_city(state_id, city_id):
    delete_city = City.delete().where(City.id == city_id, City.state == state_id)
    delete_city.execute()
    response = {}
    response['code'] = 200
    response['msg'] = "City account was deleted"
    return response, 200

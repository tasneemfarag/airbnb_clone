''' Import app and models '''
from app import app
from app.models.city import City
from app.models.city import State
from return_styles import ListStyle
from index import type_test

''' Import packages '''
from flask_json import as_json, request
from flask import abort
from datetime import datetime
import json

@app.route('/states/<state_id>/cities', methods=['GET'])
@as_json
def get_cities(state_id):
    """
    Get all cities
    List all cities in the database.
    ---
    tags:
        - City
    responses:
        200:
            description: List of all cities
            schema:
                id: Cities
                required:
                    - data
                    - paging
                properties:
                    data:
                        type: array
                        description: cities array
                        items:
                            $ref: '#/definitions/get_city_get_City'
                    paging:
                        description: pagination
                        schema:
                            $ref: '#/definitions/get_amenities_get_Paging'
    """
    try:
        ''' Check if state exists '''
        query = State.select().where(State.id == state_id)
        if not query.exists():
            raise LookupError('state')

        ''' Return list of cities in given state '''
        data = City.select().where(City.state == state_id)
        return ListStyle.list(data, request), 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        abort(500)

@app.route('/states/<state_id>/cities', methods=['POST'])
@as_json
def create_city(state_id):
    """
    Create a new city
    Create a new city in the given state.
    ---
    tags:
        - City
    parameters:
        -
            name: state_id
            in: path
            type: integer
            required: True
            description: ID of the state
        -
            name: name
            in: form
            type: string
            required: True
            description: Name of the city
    responses:
        201:
            description: City was created
            schema:
                $ref: '#/definitions/create_amenity_post_post_success'
        400:
            description: Issue with city request
        409:
            description: City already exists
        500:
            description: The request was not able to be processed
    """
    data = {}
    for key in request.form.keys():
    	for value in request.form.getlist(key):
    		data[key] = value
    try:
        ''' Check if state exists '''
        query = State.select().where(State.id == state_id)
        if not query.exists():
            raise LookupError('state_id')

        ''' Check if 'name' key in data '''
        if not 'name' in data:
            raise KeyError('name')

        ''' Check if 'name' value is a string '''
        if not type_test(data['name'], 'string'):
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
    """
    Get the given city
    Return the given city in the database.
    ---
    tags:
        - City
    parameters:
        -
            in: path
            name: state_id
            type: string
            required: True
            description: ID of the state
        -
            in: path
            name: city_id
            type: string
            required: True
            description: ID of the city
    responses:
        200:
            description: City returned successfully
            schema:
                id: City
                required:
                    - name
                    - state_id
                    - id
                    - created_at
                    - updated_at
                properties:
                    name:
                        type: string
                        description: Name of the city
                        default: "San Francisco"
                    state_id:
                        type: number
                        description: id of the state
                        default: 1
                    id:
                        type: number
                        description: id of the city
                        default: 1
                    created_at:
                        type: datetime string
                        description: date and time the city was created in the database
                        default: '2016-08-11 20:30:38'
                    updated_at:
                        type: datetime string
                        description: date and time the city was updated in the database
                        default: '2016-08-11 20:30:38'
        404:
            description: City or state was not found
        500:
            description: Request could not be processed
    """
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
    """
    Delete the given city
    Deletes the given city in the database.
    ---
    tags:
        - City
    parameters:
        -
            in: path
            name: state_id
            type: string
            required: True
            description: ID of the state
        -
            in: path
            name: city_id
            type: string
            required: True
            description: ID of the city
    responses:
        200:
            description: City deleted successfully
            schema:
                $ref: '#/definitions/delete_amenity_delete_delete_200'
        404:
            description: City was not found
        500:
            description: Request could not be processed
    """
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

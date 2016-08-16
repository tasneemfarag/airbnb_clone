''' Import app and models '''
from app import app
from app.models.state import State
from return_styles import ListStyle
from index import type_test

''' Import packages '''
from flask_json import as_json, request
from datetime import datetime
from flask import abort
import json

@app.route('/states', methods=['GET'])
@as_json
def get_states():
    try:
        ''' Returns a list of states in list named result '''
        data = State.select()
        return ListStyle.list(data, request), 200
    except Exception as e:
        abort(500)

@app.route('/states', methods=['POST'])
@as_json
def create_state():
    ''' Adds a new state '''
    data = {}
    for key in request.form.keys():
    	for value in request.form.getlist(key):
    		data[key] = value
    try:
        ''' Check that name key is in data '''
        if not 'name' in data:
            raise KeyError('name')

        ''' Check that name key is not null '''
        if not data['name']:
            raise TypeError("'name' cannot be NULL")

        ''' Check that name key value is a string '''
        if not type_test(data['name'], 'string'):
            raise TypeError("'name' must be a string")

        ''' Check if state already exists '''
        query = State.select().where(State.name == data['name'])
        if query.exists():
            raise ValueError('State already exists')

        new = State.create(
            name = data['name']
        )
        res = {}
        res['code'] = 201
        res['id'] = new.id
        res['msg'] = "State was created successfully"
        return res, 201
    except TypeError as e:
        response = {}
        response['code'] = 400
        response['msg'] = e.message
        return response, 400
    except ValueError as e:
        response = {}
        response['code'] = 10001
        response['msg'] = e.message
        return response, 409
    except KeyError as e:
        response = {}
        response['code'] = 40000
        response['msg'] = 'Missing parameters'
        return response, 400
    except Exception as e:
        print e.message
        abort(500)

@app.route('/states/<state_id>', methods=['GET'])
@as_json
def get_state(state_id):
    ''' Returns a given state '''
    try:
        ''' Check that state_id exists '''
        query = State.select().where(State.id == state_id)
        if not query.exists():
            raise LookupError('state_id')

        state = State.get(State.id == state_id)
        return state.to_dict(), 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        abort(500)

@app.route('/states/<state_id>', methods=['DELETE'])
@as_json
def delete_state(state_id):
    ''' Deletes the given state '''
    try:
        ''' Check that state_id exists '''
        query = State.select().where(State.id == state_id)
        if not query.exists():
            raise LookupError('state_id')

        ''' Delete the given state '''
        delete_state = State.delete().where(State.id == state_id)
        delete_state.execute()
        response = {}
        response['code'] = 200
        response['msg'] = "State account was deleted"
        return response, 200
    except LookupError as e:
        abort(404)
    except Exception as error:
        abort(500)

from app.models.state import State
from flask_json import as_json, request
from app import app
from datetime import datetime
from flask import abort
import json

@app.route('/states', methods=['GET'])
@as_json
def get_states():
    ''' Returns a list of states in list named result '''
    states = []
    data = State.select()
    for row in data:
        states.append(row.to_hash())
    return {"result": states}, 200

@app.route('/states', methods=['POST'])
@as_json
def create_state():
    ''' Adds a new state '''
    data = json.loads(request.data)
    try:
        if not isinstance(data['name'], unicode):
            raise ValueError("'name' must be a string")
        if not data['name']:
            raise ValueError("'name' cannot be NULL")
        new = State.create(
            name = data['name']
        )
        res = {}
        res['code'] = 201
        res['id'] = new.id
        res['msg'] = "State was created successfully"
        return res, 201
    except ValueError as e:
        response = {}
        response['code'] = 400
        response['msg'] = e.message
        return response, 400
    except KeyError as e:
        response = {}
        response['code'] = 400
        response['msg'] = str(e.message) + " is missing"
        return response, 400
    except Exception as e:
        if type(e).__name__ == 'IntegrityError':
            response = {}
            response['code'] = 10001
            response['msg'] = "State already exists"
            return response, 409
        response = {}
        response['code'] = 500
        response['msg'] = e.message
        return response, 500

@app.route('/states/<state_id>', methods=['GET'])
@as_json
def get_state(state_id):
    ''' Returns a given state '''
    try:
        state = State.get(State.id == state_id)
        return state.to_hash(), 200
    except Exception as error:
        if "Instance matching query does not exist" in error.message:
            abort(404)

@app.route('/states/<state_id>', methods=['DELETE'])
@as_json
def delete_state(state_id):
    ''' Deletes the given state '''
    try:
        delete_state = State.delete().where(State.id == state_id)
        delete_state.execute()
        response = {}
        response['code'] = 200
        response['msg'] = "State account was deleted"
        return response, 200
    except Exception as error:
        if "Instance matching query does not exist" in error.message:
            abort(404)

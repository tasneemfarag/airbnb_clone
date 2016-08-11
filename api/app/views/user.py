''' Import app and models '''
from app import app
from app.models.user import User

''' Import packages '''
from flask_json import as_json, request
from datetime import datetime
from flask import abort
import json

@app.route('/users', methods=['GET'])
@as_json
def get_users():
    ''' Returns all users in list named result '''
    users = []
    data = User.select()
    for row in data:
        users.append(row.to_dict())
    return {"result": users}, 200

@app.route('/users', methods=['POST'])
@as_json
def create_user():

    ''' Creates a new user '''
    try:
        data = json.loads(request.data)

        ''' Test for required keys '''
        if not 'email' in data:
            raise KeyError('email')
        if not 'first_name' in data:
            raise KeyError('first_name')
        if not 'last_name' in data:
            raise KeyError('last_name')
        if not 'password' in data:
            raise KeyError('password')

        ''' Test required key value data types '''
        if not isinstance(data['email'], unicode):
            raise TypeError('email is not a string')
        if not isinstance(data['first_name'], unicode):
            raise TypeError('first_name is not a string')
        if not isinstance(data['last_name'], unicode):
            raise TypeError('last_name is not a string')
        if not isinstance(data['password'], unicode):
            raise TypeError('password is not a string')

        ''' Test optional key value data types '''
        if 'is_admin' in data and not isinstance(data['is_admin'], bool):
            raise TypeError('is_admin is not a boolean value')

        ''' Test if email already exists in the db '''
        query = User.select().where(User.email == data['email'])
        if query.exists():
            raise ValueError('Email already exists')

        new = User(
            email = data['email'],
            first_name = data['first_name'],
            last_name = data['last_name']
        )
        if 'is_admin' in data:
            new.is_admin = data['is_admin']
        new.set_password(data['password'])
        new.save()
        res = {}
        res['code'] = 201
        res['msg'] = "User was created successfully"
        res['id'] = new.id
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
        res['code'] = 10000
        res['msg'] = "Email already exists"
        return res, 409
    except Exception as e:
        abort(500)

@app.route('/users/<user_id>', methods=['GET'])
@as_json
def get_user(user_id):
    ''' Returns a specific user '''
    try:
        ''' Check if user_id exists '''
        query = User.select().where(User.id == user_id)
        if not query.exists():
            raise LookupError('user_id')

        ''' Return user data '''
        user = User.get(User.id == user_id)
        return user.to_dict(), 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        abort(500)

@app.route('/users/<user_id>', methods=['PUT'])
@as_json
def update_user(user_id):
    ''' Updates user information '''
    data = json.loads(request.data)
    try:
        ''' Check if protected fields are included '''
        if 'email' in data:
            raise ValueError("Email cannot be changed")

        ''' Check for valid data types '''
        if 'first_name' in data and not isinstance(data['first_name'], unicode):
            raise TypeError('first_name is not a string')
        if 'last_name' in data and not isinstance(data['last_name'], unicode):
            raise TypeError('last_name is not a string')
        if 'is_admin' in data and not isinstance(data['is_admin'], bool):
            raise TypeError('is_admin is not a boolean value')
        if 'password' in data and not isinstance(data['password'], unicode):
            raise TypeError('password is not a string')

        ''' Check if user_id exists '''
        query = User.select().where(User.id == user_id)
        if not query.exists():
            raise LookupError('user_id')

        ''' Retrieve user record and update '''
        user = User.get(User.id == user_id)
        for key in data:
            if key == 'first_name':
                user.first_name = data['first_name']
            elif key == 'last_name':
                user.last_name = data['last_name']
            elif key == 'is_admin':
                user.is_admin = data['is_admin']
            elif key == 'password':
                user.set_password(data['password'])
        user.save()
        res = {}
        res['code'] = 200
        res['msg'] = "User was updated successfully"
        return res, 200
    except TypeError as e:
        res = {}
        res['code'] = 400
        res['msg'] = e.message
        return res, 400
    except ValueError as e:
        res = {}
        res['code'] = 403
        res['msg'] = e.message
        return res, 403
    except LookupError as e:
        abort(404)
    except Exception as error:
        abort(500)

@app.route('/users/<user_id>', methods=['DELETE'])
@as_json
def delete_user(user_id):
    ''' Deletes a specific user '''
    try:
        ''' Check if user_id exists '''
        query = User.select().where(User.id == user_id)
        if not query.exists():
            raise LookupError('user_id')

        ''' Delete the given user '''
        delete_user = User.delete().where(User.id == user_id)
        delete_user.execute()
        response = {}
        response['code'] = 200
        response['msg'] = "User account was deleted"
        return response, 200
    except LookupError as e:
        abort(404)
    except Exception as error:
        abort(500)

''' Import app and models '''
from app import app
from app.models.user import User
from return_styles import ListStyle
from index import type_test

''' Import packages '''
from flask_json import as_json, request
from datetime import datetime
from flask import abort
import json

@app.route('/users', methods=['GET'])
@as_json
def get_users():
    ''' Returns all users in list named result '''
    data = User.select()
    return ListStyle.list(data, request), 200

@app.route('/users', methods=['POST'])
@as_json
def create_user():

    ''' Creates a new user '''
    try:
        data = {}
        for key in request.form.keys():
           for value in request.form.getlist(key):
               data[key] = value

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
        if not type_test(data['email'], 'email'):
            raise TypeError('email is not valid')
        if not type_test(data['first_name'], 'string'):
            raise TypeError('first_name is not a string')
        if not type_test(data['last_name'], 'string'):
            raise TypeError('last_name is not a string')
        if not type_test(data['password'], 'string'):
            raise TypeError('password is not a string')

        ''' Test optional key value data types '''
        if 'is_admin' in data:
            if not type_test(data['is_admin'], bool):
                raise TypeError('is_admin is not a True or False value')

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
    data = {}
    for key in request.form.keys():
    	for value in request.form.getlist(key):
    		data[key] = value
    try:
        ''' Check if protected fields are included '''
        if 'email' in data:
            raise ValueError("Email cannot be changed")

        ''' Check for valid data types '''
        if 'first_name' in data and not type_test(data['first_name'], 'string'):
            raise TypeError('first_name is not a string')
        if 'last_name' in data and not type_test(data['last_name'], 'string'):
            raise TypeError('last_name is not a string')
        if 'is_admin' in data and not type_test(data['is_admin'], bool):
            raise TypeError('is_admin is not a boolean value')
        if 'password' in data and not type_test(data['password'], 'string'):
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
                if data['is_admin'] == 'True':
                    user.is_admin = True
                else:
                    user.is_admin = False
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

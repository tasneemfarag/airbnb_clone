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
    """
    Get all users
    List all users in the database.
    ---
    tags:
        - User
    responses:
        200:
            description: List of all users
            schema:
                id: Users
                required:
                    - data
                    - paging
                properties:
                    data:
                        type: array
                        description: users array
                        items:
                            $ref: '#/definitions/get_user_get_User'
                    paging:
                        description: pagination
                        schema:
                            $ref: '#/definitions/get_amenities_get_Paging'
    """
    data = User.select()
    return ListStyle.list(data, request), 200

@app.route('/users', methods=['POST'])
@as_json
def create_user():
    """
    Create a new user
    Create a new user in the database
    ---
    tags:
        - User
    parameters:
        -
            name: email
            in: form
            type: string
            required: True
            description: Email of the user
        -
            name: first_name
            in: form
            type: string
            required: True
            description: First name of the user
        -
            name: last_name
            in: form
            type: string
            required: True
            description: Last name of the user
        -
            name: is_admin
            in: form
            type: boolean
            description: Defines if the user is an admin
        -
            name: password
            in: form
            type: string
            required: True
            description: Password for the user
    responses:
        201:
            description: User was created
            schema:
                $ref: '#/definitions/create_amenity_post_post_success'
        400:
            description: Issue with user request
        409:
            description: Email already exists
        500:
            description: The request was not able to be processed
    """
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
    """
    Get the given user
    Returns the given user in the database.
    ---
    tags:
    	- User
    parameters:
    	-
    		in: path
    		name: user_id
    		type: integer
    		required: True
    		description: ID of the user
    responses:
        200:
            description: User returned successfully
            schema:
                id: User
                required:
                    - email
                    - first_name
                    - last_name
                    - password
                    - id
                    - created_at
                    - updated_at
                properties:
                    first_name:
                        type: string
                        description: First name of the user
                        default: "Jon"
                    last_name:
                        type: string
                        description: Last name of the user
                        default: "Snow"
                    email:
                        type: string
                        description: Email address of the user
                        default: "jon.snow@gmail.com"
                    is_admin:
                        type: bool
                        description: Define if the user is an admin or not
                        default: False
                    id:
                        type: number
                        description: id of the user
                        default: 1
                    created_at:
                        type: datetime string
                        description: date and time the user was created in the database
                        default: '2016-08-11 20:30:38.959846'
                    updated_at:
                        type: datetime string
                        description: date and time the user was updated in the database
                        default: '2016-08-11 20:30:38.959846'
        404:
            description: User was not found
        500:
            description: Request could not be processed
    """
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
    """
    Update a user
    Update a user in the database
    ---
    tags:
        - User
    parameters:
        -
            name: first_name
            in: form
            type: string
            description: First name of the user
        -
            name: last_name
            in: form
            type: string
            description: Last name of the user
        -
            name: is_admin
            in: form
            type: boolean
            description: Defines if the user is an admin
        -
            name: password
            in: form
            type: string
            description: Password for the user
    responses:
        200:
            description: User was updated
            schema:
                $ref: '#/definitions/update_booking_put_put_success'
        400:
            description: Issue with user update request
        403:
            description: Email cannot be changed
        500:
            description: The request was not able to be processed
    """
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
    """
    Delete the given user
    Deletes the given user in the database.
    ---
    tags:
        - User
    parameters:
        -
            in: path
            name: user_id
            type: string
            required: True
            description: ID of the user
    responses:
        200:
            description: User deleted successfully
            schema:
                $ref: '#/definitions/delete_amenity_delete_delete_200'
        404:
            description: User was not found
        500:
            description: Request could not be processed
    """
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

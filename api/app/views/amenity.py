# -*- coding: utf-8 -*-

''' Import app and models '''
from app import app
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.place_amenity import PlaceAmenities
from return_styles import ListStyle
from index import type_test

''' Import packages '''
from flask_json import as_json, request
from flask import abort
from datetime import datetime
from peewee import OperationalError
import json

@app.route('/amenities', methods=['GET'])
@as_json
def get_amenities():
    """
    Get all amenities
    List all amenities in the database.
    ---
    tags:
        - Amenity
    responses:
        200:
            description: List of all amenities
            schema:
                id: Amenities
                required:
                    - data
                    - paging
                properties:
                    data:
                        type: array
                        description: amenities array
                        items:
                            $ref: '#/definitions/get_amenity_get_Amenity'
                    paging:
                        description: pagination
                        schema:
                            id: Paging
                            required:
                                - next
                                - prev
                            properties:
                                next:
                                    type: string
                                    description: next page URL
                                    default: "/<path>?page=3&number=10"
                                prev:
                                    type: string
                                    description: previous page URL
                                    default: "/<path>?page=1&number=10"
    """
    data = Amenity.select()
    return ListStyle.list(data, request), 200

@app.route('/amenities', methods=['POST'])
@as_json
def create_amenity():
    """
    Create a new amenity
    Create a new amenity in the database.
    ---
    tags:
        - Amenity
    parameters:
        -
            name: name
            in: form
            type: string
            required: True
            description: Name of the amenity
    responses:
        201:
            description: Amenity was created
            schema:
                id: post_success
                required:
                    - code
                    - id
                    - msg
                properties:
                    code:
                        type: integer
                        description: Response code from the API
                        default: 201
                    id:
                        type: integer
                        description: ID of the newly created record
                        default: 1
                    msg:
                        type: string
                        description: Message about record creation
                        default: "created successfully"
        400:
            description: Issue with amenity request
        409:
            description: Amenity already exists
        500:
            description: The request was not able to be processed
    """
    data = {}
    if request.json:
        data = request.json
    else:
        for key in request.form.keys():
        	for value in request.form.getlist(key):
        		data[key] = value
    try:
        ''' Check if name for amenity was given '''
        if not 'name' in data:
            raise KeyError("'name'")

        ''' Check if name is a string '''
        if not type_test(data['name'], 'string'):
            raise TypeError("amenity 'name' must be a string value")

        ''' Check if amenity already exists '''
        query = Amenity.select().where(Amenity.name == data['name'])
        if query.exists():
            raise ValueError('amenity already exists')

        ''' Create new amenity '''
        new = Amenity.create(
            name = data['name']
        )
        res = {}
        res['code'] = 201
        res['id'] = new.id
        res['msg'] = "amenity was created successfully"
        return res, 201
    except KeyError as e:
        print data
        res = {}
        res['code'] = 40000
        res['msg'] = 'missing parameters'
        return res, 400
    except TypeError as e:
        res = {}
        res['code'] = 400
        res['msg'] = e.message
        return res, 400
    except ValueError as e:
        res = {}
        res['code'] = 10003
        res['msg'] = e.message
        return res, 409
    except Exception as e:
        abort(500)

@app.route('/amenities/<amenity_id>', methods=['GET'])
@as_json
def get_amenity(amenity_id):
    """
    Get the given amenity
    Return the given amenity in the database.
    ---
    tags:
        - Amenity
    parameters:
        -
            in: path
            name: amenity_id
            type: string
            required: True
            description: ID of the amenity
    responses:
        200:
            description: Amenity returned successfully
            schema:
                id: Amenity
                required:
                    - name
                    - id
                    - created_at
                    - updated_at
                properties:
                    name:
                        type: string
                        description: Name of the amenity
                        default: "Swimming Pool"
                    id:
                        type: number
                        description: id of the amenity
                        default: 1
                    created_at:
                        type: datetime string
                        description: date and time the amenity was created in the database
                        default: '2016-08-11 20:30:38'
                    updated_at:
                        type: datetime string
                        description: date and time the amenity was updated in the database
                        default: '2016-08-11 20:30:38'
        404:
            description: Amenity was not found
        500:
            description: Request could not be processed
    """
    try:
        ''' Check if amenity exists '''
        query = Amenity.select().where(Amenity.id == amenity_id)
        if not query.exists():
            raise LookupError('amenity_id')

        ''' Return amenity data '''
        amenity = Amenity.get(Amenity.id == amenity_id)
        return amenity.to_dict(), 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        abort(500)

@app.route('/amenities/<amenity_id>', methods=['DELETE'])
@as_json
def delete_amenity(amenity_id):
    """
    Delete the given amenity
    Deletes the given amenity in the database.
    ---
    tags:
        - Amenity
    parameters:
        -
            in: path
            name: amenity_id
            type: string
            required: True
            description: ID of the amenity
    responses:
        200:
            description: Amenity deleted successfully
            schema:
                id: delete_200
                required:
                    - code
                    - msg
                properties:
                    code:
                        type: integer
                        description: Response code from the API
                        default: 200
                    msg:
                        type: string
                        description: Message about record deletion
                        default: "deleted successfully"
        404:
            description: Amenity was not found
        500:
            description: Request could not be processed
    """
    try:
        ''' Check if amenity exists '''
        query = Amenity.select().where(Amenity.id == amenity_id)
        if not query.exists():
            raise LookupError('amenity_id')

        ''' Delete the amenity '''
        amenity = Amenity.delete().where(Amenity.id == amenity_id)
        amenity.execute()
        res = {}
        res['code'] = 200
        res['msg'] = "Amenity was deleted successfully"
        return res, 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        abort(500)

@app.route('/places/<place_id>/amenities', methods=['GET'])
@as_json
def get_place_amenities(place_id):
    """
    Get amenities for place
    Return a list of all amenities for a place
    ---
    tags:
        - Amenity
    parameters:
        -
            in: path
            name: place_id
            type: string
            required: True
            description: ID of the place
    responses:
        200:
            description: List of all amenities for the place
            schema:
                $ref: '#/definitions/get_amenities_get_Amenities'
    """
    try:
        ''' Check if the place exists '''
        query = Place.select().where(Place.id == place_id)
        if not query.exists():
            raise LookupError('place_id')

        ''' Return amenities for the given place '''
        data = Amenity.select().join(PlaceAmenities).where(PlaceAmenities.place == place_id)
        return ListStyle.list(data, request), 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        abort(500)

@app.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
@as_json
def post_place_amenity(place_id, amenity_id):
    """
    Create a new amenity for place
    Create a new amenity in the database for the given place
    ---
    tags:
        - Amenity
    parameters:
        -
            name: place_id
            in: path
            type: string
            required: True
            description: ID of the given place
        -
            name: amenity_id
            in: path
            type: string
            required: True
            description: ID of the given amenity
    responses:
        201:
            description: Amenity was created
            schema:
                $ref: '#/definitions/create_amenity_post_post_success'
        400:
            description: Issue with amenity request
        409:
            description: Amenity already exists
        500:
            description: The request was not able to be processed
    """
    try:
        ''' Check if place_id is valid '''
        query = Place.select().where(Place.id == place_id)
        if not query.exists():
            raise LookupError('place_id')

        ''' Check if amenity_id is valid '''
        query = Amenity.select().where(Amenity.id == amenity_id)
        if not query.exists():
            raise LookupError('amenity_id')

        ''' Check if amenity is already added for place '''
        query = PlaceAmenities.select().where(PlaceAmenities.amenity == amenity_id, PlaceAmenities.place == place_id)
        if query.exists():
            raise ValueError('Amenity is already set for the given place')

        ''' Add amenity for place '''
        new = PlaceAmenities.create(
            place = place_id,
            amenity = amenity_id
        )
        res = {
            'code': 201,
            'msg': 'Amenity added successfully for the given place'
        }
        return res, 201
    except LookupError as e:
        abort(404)
    except ValueError as e:
        res = {}
        res['code'] = 400
        res['msg'] = e.message
        return res, res['code']
    except Exception as e:
        abort(500)

@app.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
@as_json
def delete_place_amenity(place_id, amenity_id):
    """
    Delete the given amenity
    Deletes the given amenity in the database.
    ---
    tags:
        - Amenity
    parameters:
        -
            name: place_id
            in: path
            type: string
            required: True
            description: ID of the given place
        -
            name: amenity_id
            in: path
            type: string
            required: True
            description: ID of the given amenity
    responses:
        200:
            description: Amenity deleted successfully
            schema:
                $ref: '#/definitions/delete_amenity_delete_delete_200'
                required:
                    - code
                    - msg
        404:
            description: Amenity was not found
        500:
            description: Request could not be processed
    """
    try:
        ''' Check if place_id is valid '''
        query = Place.select().where(Place.id == place_id)
        if not query.exists():
            raise LookupError('place_id')

        ''' Check if amenity_id is valid '''
        query = Amenity.select().where(Amenity.id == amenity_id)
        if not query.exists():
            raise LookupError('amenity_id')

        ''' Check if amenity is already added for place '''
        query = PlaceAmenities.select().where(PlaceAmenities.amenity == amenity_id, PlaceAmenities.place == place_id)
        if not query.exists():
            raise LookupError('amenity_id, place_id')

        ''' Add amenity for place '''
        delete = PlaceAmenities.delete().where(
            PlaceAmenities.amenity == amenity_id,
            PlaceAmenities.place == place_id
        )
        delete.execute()
        res = {}
        res['code'] = 200
        res['msg'] = 'Amenity deleted successfully for the given place'
        return res, 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        abort(500)

''' Import app and models '''
from app import app
from app.models.place import Place
from app.models.city import City
from app.models.state import State
from app.models.user import User
from app.models.place_book import PlaceBook
from return_styles import ListStyle
from index import type_test

''' Import packages '''
from flask_json import as_json, request
from datetime import datetime, timedelta
from flask import abort
import json

@app.route('/places', methods=['GET'])
@as_json
def get_places():
    """
    Get all places
    List all places in the database.
    ---
    tags:
        - Place
    responses:
        200:
            description: List of all places
            schema:
                id: Places
                required:
                    - data
                    - paging
                properties:
                    data:
                        type: array
                        description: places array
                        items:
                            $ref: '#/definitions/get_place_get_Place'
                    paging:
                        description: pagination
                        schema:
                            $ref: '#/definitions/get_amenities_get_Paging'
    """
    data = Place.select()
    return ListStyle.list(data, request), 200

@app.route('/places', methods=['POST'])
@as_json
def create_place():
    """
    Create a new place
    Create a new place in the database
    ---
    tags:
        - Place
    parameters:
        -
            name: owner_id
            in: form
            type: integer
            required: True
            description: user id of the owner
        -
            name: city_id
            in: form
            type: integer
            required: True
            description: id of the city
        -
            name: name
            in: form
            type: string
            required: True
            description: name of the place
        -
            name: description
            in: form
            type: string
            description: description of the place
        -
            name: number_rooms
            in: form
            type: integer
            description: number of rooms
        -
            name: number_bathrooms
            in: form
            type: integer
            description: number of bathrooms
        -
            name: max_guest
            in: form
            type: integer
            description: the max number of guests
        -
            name: price_by_night
            in: form
            type: integer
            description: the price per night of the location
        -
            name: latitude
            in: form
            type: float
            description: the latitude of the place location
        -
            name: longitude
            in: form
            type: float
            description: the longitude of the place location
    responses:
        201:
            description: Place was created
            schema:
                $ref: '#/definitions/create_amenity_post_post_success'
        400:
            description: Issue with place request
        404:
            description: Owner or city was not found
        500:
            description: The request was not able to be processed
    """
    data = {}
    for key in request.form.keys():
    	for value in request.form.getlist(key):
    		data[key] = value
    try:
        ''' Check for required keys '''
        if not 'owner_id' in data:
            raise KeyError('owner_id')
        if not 'name' in data:
            raise KeyError('name')
        if not 'city_id' in data:
            raise KeyError('city_id')

        ''' Check required key value data types '''
        if not type_test(data['owner_id'], int):
            raise TypeError('owner_id is not an integer')
        if not type_test(data['name'], 'string'):
            raise TypeError('name is not a string')
        if not type_test(data['city_id'], int):
            raise TypeError('city_id is not an integer')

        ''' Check optional key value data types '''
        if 'description' in data and not type_test(data['description'], 'string'):
            raise TypeError('description is not a string')
        if 'number_rooms' in data and not type_test(data['number_rooms'], int):
            raise TypeError('number_rooms is not an integer')
        if 'number_bathrooms' in data and not type_test(data['number_bathrooms'], int):
            raise TypeError('number_bathrooms is not an integer')
        if 'max_guest' in data and not type_test(data['max_guest'], int):
            raise TypeError('max_guest is not an integer')
        if 'price_by_night' in data and not type_test(data['price_by_night'], int):
            raise TypeError('price_by_night is not an integer')
        if 'latitude' in data and not type_test(data['latitude'], float):
            raise TypeError('latitude is not a float')
        if 'longitude' in data and not type_test(data['longitude'], float):
            raise TypeError('longitude is not a float')

        ''' Check if city_id exists '''
        query = City.select().where(City.id == data['city_id'])
        if not query.exists():
            raise LookupError('city_id')

        ''' Check if owner_id exists '''
        query = User.select().where(User.id == data['owner_id'])
        if not query.exists():
            raise LookupError('owner_id')


        ''' Creates a new place '''
        new = Place(
            owner = data['owner_id'],
            name = data['name'],
            city = data['city_id']
        )
        if data['description']:
            new.description = data['description']
        if data['number_rooms']:
            new.number_rooms = data['number_rooms']
        if data['number_bathrooms']:
            new.number_bathrooms = data['number_bathrooms']
        if data['max_guest']:
            new.max_guest = data['max_guest']
        if data['price_by_night']:
            new.price_by_night = data['price_by_night']
        if data['latitude']:
            new.latitude = data['latitude']
        if data['longitude']:
            new.longitude = data['longitude']
        new.save()
        res = {}
        res['code'] = 201
        res['id'] = new.id
        res['msg'] = "Place was created successfully"
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
    except LookupError as e:
        abort(404)
    except Exception as e:
        abort(500)

@app.route('/places/<place_id>', methods=['GET'])
@as_json
def get_place(place_id):
    """
    Get the given place
    Returns the given place in the database.
    ---
    tags:
        - Place
    parameters:
        -
            in: path
            name: place_id
            type: integer
            required: True
            description: ID of the place
    responses:
        200:
            description: Place returned successfully
            schema:
                id: Place
                required:
                    - owner_id
                    - city_id
                    - name
                    - id
                    - created_at
                    - updated_at
                properties:
                    owner_id:
                        type: integer
                        description: user id of the owner
                        default: 1
                    city_id:
                        type: integer
                        description: id of the city
                        default: 1
                    name:
                        type: string
                        description: name of the place
                        default: 'Amazing view near San Francisco'
                    description:
                        type: string
                        description: description of the place
                        default: "The place is located on the ocean's edge... literally."
                    number_rooms:
                        type: integer
                        description: number of rooms
                        default: 3
                    number_bathrooms:
                        type: integer
                        description: number of bathrooms
                        default: 2
                    max_guest:
                        type: integer
                        description: the max number of guests
                        default: 6
                    price_by_night:
                        type: integer
                        description: the price per night of the location
                        default: 200
                    latitude:
                        type: float
                        description: the latitude of the place location
                        default: 37.642357
                    longitude:
                        type: float
                        description: the longitude of the place location
                        default: -122.493439
                    id:
                        type: integer
                        description: id of the place
                        default: 1
                    created_at:
                        type: datetime string
                        description: date and time the booking was created in the database
                        default: '2016-08-11 20:30:38'
                    updated_at:
                        type: datetime string
                        description: date and time the booking was updated in the database
                        default: '2016-08-11 20:30:38'
        404:
            description: Place, owner or city was not found
        500:
            description: Request could not be processed
    """
    try:
        ''' Check if place_id exists '''
        query = Place.select().where(Place.id == place_id)
        if not query.exists():
            raise LookupError('place_id')

        ''' Return place data '''
        place = Place.get(Place.id == place_id)
        return place.to_dict(), 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        abort(500)

@app.route('/places/<place_id>', methods=['PUT'])
@as_json
def update_place(place_id):
    """
    Update a place
    Update a place in the database
    ---
    tags:
        - Place
    parameters:
        -
            name: place_id
            in: path
            type: integer
            required: True
            description: ID of the place
        -
            name: name
            in: form
            type: string
            description: name of the place
        -
            name: description
            in: form
            type: string
            description: description of the place
        -
            name: number_rooms
            in: form
            type: integer
            description: number of rooms
        -
            name: number_bathrooms
            in: form
            type: integer
            description: number of bathrooms
        -
            name: max_guest
            in: form
            type: integer
            description: the max number of guests
        -
            name: price_by_night
            in: form
            type: integer
            description: the price per night of the location
        -
            name: latitude
            in: form
            type: float
            description: the latitude of the place location
        -
            name: longitude
            in: form
            type: float
            description: the longitude of the place location
    responses:
        200:
            description: Place was updated
            schema:
                $ref: '#/definitions/update_booking_put_put_success'
        400:
            description: Issue with booking update request
        404:
            description: Place was not found
        410:
            description: Place is unavailable for the requested booking
        500:
            description: The request was not able to be processed
    """
    try:
        data = {}
        for key in request.form.keys():
        	for value in request.form.getlist(key):
        		data[key] = value

        ''' Check if place_id exists '''
        query = Place.select().where(Place.id == place_id)
        if not query.exists():
            raise LookupError('place_id')

        ''' Check that no request to change protected values '''
        if 'owner_id' in data:
            raise ValueError('Owner cannot be changed')
        if 'city_id' in data:
            raise ValueError('City cannot be changed')

        ''' Check for valid data types '''
        if 'name' in data and not type_test(data['name'], 'string'):
            raise TypeError('name is not a string')
        if 'description' in data and not type_test(data['description'], 'string'):
            raise TypeError('description is not a string')
        if 'number_rooms' in data and not type_test(data['number_rooms'], int):
            raise TypeError('number_rooms is not an integer')
        if 'number_bathrooms' in data and not type_test(data['number_bathrooms'], int):
            raise TypeError('number_bathrooms is not an integer')
        if 'max_guest' in data and not type_test(data['max_guest'], int):
            raise TypeError('max_guest is not an integer')
        if 'price_by_night' in data and not type_test(data['price_by_night'], int):
            raise TypeError('price_by_night is not an integer')
        if 'latitude' in data and not type_test(data['latitude'], float):
            raise TypeError('latitude is not a float')
        if 'longitude' in data and not type_test(data['longitude'], float):
            raise TypeError('longitude is not a float')

        place = Place.get(Place.id == place_id)
        for key in data:
            if key == 'name':
                place.name = data[key]
            elif key == 'description':
                place.description = data[key]
            elif key == 'number_rooms':
                place.number_rooms = data[key]
            elif key == 'number_bathrooms':
                place.number_bathrooms = data[key]
            elif key == 'max_guest':
                place.max_guest = data[key]
            elif key == 'price_by_night':
                place.price_by_night = data[key]
            elif key == 'latitude':
                place.latitude = data[key]
            elif key == 'longitude':
                place.longitude = data[key]
        place.save()
        res = {}
        res['code'] = 200
        res['msg'] = "Place was updated successfully"
        return res, 200
    except ValueError as e:
        res = {}
        res['code'] = 403
        res['msg'] = e.message
        return res, 403
    except LookupError as e:
        abort(404)
    except TypeError as e:
        res = {}
        res['code'] = 400
        res['msg'] = e.message
        return res, 400
    except Exception as error:
        abort(500)

@app.route('/places/<place_id>', methods=['DELETE'])
@as_json
def delete_place(place_id):
    """
    Delete the given place
    Deletes the given place in the database.
    ---
    tags:
        - Place
    parameters:
        -
            in: path
            name: place_id
            type: integer
            required: True
            description: ID of the place
    responses:
        200:
            description: Place deleted successfully
            schema:
                $ref: '#/definitions/delete_amenity_delete_delete_200'
        404:
            description: Place was not found
        500:
            description: Request could not be processed
    """
    try:
        ''' Check if place_id exists '''
        query = Place.select().where(Place.id == place_id)
        if not query.exists():
            raise LookupError('place_id')

        ''' Delete the given place '''
        delete_place = Place.delete().where(Place.id == place_id)
        delete_place.execute()
        response = {}
        response['code'] = 200
        response['msg'] = "Place was deleted"
        return response, 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        abort(505)

@app.route('/states/<state_id>/cities/<city_id>/places', methods=['GET'])
@as_json
def get_places_by_city(state_id, city_id):
    """
    Get all places
    List all places in the given city in the database.
    ---
    tags:
        - Place
    parameters:
        -
            name: state_id
            in: path
            type: integer
            required: True
            description: ID of the state
        -
            name: city_id
            in: path
            type: integer
            required: True
            description: ID of the city
    responses:
        200:
            description: List of all places
            schema:
                $ref: '#/definitions/get_places_get_Places'
    """
    try:
        ''' Check if the state_id exists '''
        query = State.select().where(State.id == state_id)
        if not query.exists():
            raise LookupError('state_id')

        ''' Check if the city_id exists '''
        query = City.select().where(City.id == city_id)
        if not query.exists():
            raise LookupError('city_id')

        ''' Check if the city_id is associated to the state_id '''
        city = City.get(City.id == city_id)
        query = State.select().where(State.id == city.state, State.id == state_id)
        if not query.exists():
            raise LookupError('city_id, state_id')

        ''' Return all places in the given city '''
        data = Place.select().where(Place.city == city.id)
        return ListStyle.list(data, request), 200
    except LookupError as e:
        abort(404)
    except Exception as error:
        abort(500)

@app.route('/states/<state_id>/cities/<city_id>/places', methods=['POST'])
@as_json
def create_place_by_city(state_id, city_id):
    """
    Create a new place
    Create a new place in the given city
    ---
    tags:
        - Place
    parameters:
        -
            name: state_id
            in: path
            type: integer
            required: True
            description: id of the state
        -
            name: city_id
            in: path
            type: integer
            required: True
            description: id of the city
        -
            name: owner_id
            in: form
            type: integer
            required: True
            description: user id of the owner
        -
            name: name
            in: form
            type: string
            required: True
            description: name of the place
        -
            name: description
            in: form
            type: string
            description: description of the place
        -
            name: number_rooms
            in: form
            type: integer
            description: number of rooms
        -
            name: number_bathrooms
            in: form
            type: integer
            description: number of bathrooms
        -
            name: max_guest
            in: form
            type: integer
            description: the max number of guests
        -
            name: price_by_night
            in: form
            type: integer
            description: the price per night of the location
        -
            name: latitude
            in: form
            type: float
            description: the latitude of the place location
        -
            name: longitude
            in: form
            type: float
            description: the longitude of the place location
    responses:
        201:
            description: Place was created
            schema:
                $ref: '#/definitions/create_amenity_post_post_success'
        400:
            description: Issue with place request
        404:
            description: Owner or city was not found
        500:
            description: The request was not able to be processed
    """
    try:
        data = {}
        for key in request.form.keys():
        	for value in request.form.getlist(key):
        		data[key] = value

        ''' Check for required keys '''
        if not 'owner_id' in data:
            raise KeyError('owner_id')
        if not 'name' in data:
            raise KeyError('name')

        ''' Check required key value data types '''
        if not type_test(data['owner_id'], int):
            raise TypeError('owner_id is not an integer')
        if not type_test(data['name'], 'string'):
            raise TypeError('name is not a string')

        ''' Check optional key value data types '''
        if 'description' in data and not type_test(data['description'], 'string'):
            raise TypeError('description is not a string')
        if 'number_rooms' in data and not type_test(data['number_rooms'], int):
            raise TypeError('number_rooms is not an integer')
        if 'number_bathrooms' in data and not type_test(data['number_bathrooms'], int):
            raise TypeError('number_bathrooms is not an integer')
        if 'max_guest' in data and not type_test(data['max_guest'], int):
            raise TypeError('max_guest is not an integer')
        if 'price_by_night' in data and not type_test(data['price_by_night'], int):
            raise TypeError('price_by_night is not an integer')
        if 'latitude' in data and not type_test(data['latitude'], float):
            raise TypeError('latitude is not a float')
        if 'longitude' in data and not type_test(data['longitude'], float):
            raise TypeError('longitude is not a float')

        ''' Check if the state_id exists '''
        query = State.select().where(State.id == state_id)
        if not query.exists():
            raise LookupError('state_id')

        ''' Check if the city_id exists '''
        query = City.select().where(City.id == city_id)
        if not query.exists():
            raise LookupError('city_id')

        ''' Check if the city_id is associated to the state_id '''
        city = City.get(City.id == city_id)
        query = State.select().where(State.id == city.state, State.id == state_id)
        if not query.exists():
            raise LookupError('city_id, state_id')

        ''' Check if the owner_id exists '''
        query = User.select().where(User.id == data['owner_id'])
        if not query.exists():
            raise LookupError('owner_id')

        new = Place(
            owner = data['owner_id'],
            name = data['name'],
            city = city.id
        )
        if data['description']:
            new.description = data['description']
        if data['number_rooms']:
            new.number_rooms = data['number_rooms']
        if data['number_bathrooms']:
            new.number_bathrooms = data['number_bathrooms']
        if data['max_guest']:
            new.max_guest = data['max_guest']
        if data['price_by_night']:
            new.price_by_night = data['price_by_night']
        if data['latitude']:
            new.latitude = data['latitude']
        if data['longitude']:
            new.longitude = data['longitude']
        new.save()
        res = {}
        res['code'] = 201
        res['id'] = new.id
        res['msg'] = "Place was created successfully"
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
    except Exception as e:
        print e.message
        abort(500)

@app.route('/states/<state_id>/places', methods=['GET'])
@as_json
def get_places_by_state(state_id):
    """
    Get all places by state
    List all places in the given state in the database.
    ---
    tags:
        - Place
    parameters:
        -
            name: state_id
            in: path
            type: integer
            required: True
            description: ID of the state
    responses:
        200:
            description: List of all places in state
            schema:
                $ref: '#/definitions/get_places_get_Places'
    """
    try:
        ''' Check if state exists '''
        query = State.select().where(State.id == state_id)
        if not query.exists():
            raise LookupError('state_id')

        ''' Create a list of city ids in the state '''
        query = City.select().where(City.state == state_id)
        if not query.exists():
            return ListStyle.list(query, request), 200
        cities = []
        for city in query:
            cities.append(city.id)

        ''' Return the places in listed cities '''
        data = Place.select().where(Place.city << cities)
        return ListStyle.list(data, request), 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        print e.message
        abort(500)

@app.route('/places/<place_id>/available', methods=['POST'])
@as_json
def get_place_availability(place_id):
    """
    Checks availability of a place
    Returns the availability of a place based on current bookings
    ---
    tags:
        - Place
    parameters:
        -
            name: place_id
            in: path
            type: integer
            required: True
            description: id of the place
        -
            name: year
            in: form
            type: integer
            required: True
            description: year of the requested date
        -
            name: month
            in: form
            type: integer
            required: True
            description: month of the requested date
        -
            name: day
            in: form
            type: integer
            required: True
            description: day of the requested date
    responses:
        200:
            description: Place availability was returned
            schema:
                id: availability
                required:
                    - available
                properties:
                    available:
                        type: boolean
                        description: availability of the place
                        default: False
        400:
            description: Issue with place availability request
        404:
            description: Place was not found
        500:
            description: The request was not able to be processed
    """
    try:
        data = {}
        for key in request.form.keys():
        	for value in request.form.getlist(key):
        		data[key] = value
        ''' Check for required keys '''
        if not 'year' in data:
            raise KeyError('year')
        if not 'month' in data:
            raise KeyError('month')
        if not 'day' in data:
            raise KeyError('day')

        ''' Check for valid data types '''
        if not type_test(data['year'], int):
            raise TypeError('year')
        if not type_test(data['month'], int):
            raise TypeError('month')
        if not type_test(data['day'], int):
            raise TypeError('day')
        ''' Check if place exists '''
        query = Place.select().where(Place.id == place_id)
        if not query.exists():
            raise LookupError('place_id')

        ''' Set datetime object to compare '''
        check_date = datetime(int(data['year']), int(data['month']), int(data['day']))

        ''' Check if date is already booked '''
        bookings = PlaceBook.select().where(PlaceBook.place == place_id)
        for booking in bookings:
            date_start = booking.date_start.replace(hour=0, minute=0, second=0)
            date_end = date_start + timedelta(days= int(booking.number_nights))
            if check_date >= date_start and check_date < date_end:
                return {'available': False}, 200
        return {'available': True}, 200
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
        res['msg'] = str(e.message) + 'is not an integer'
        return res, 400
    except Exception as e:
        print e.message
        abort(500)

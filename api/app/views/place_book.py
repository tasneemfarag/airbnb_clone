''' Import app and models '''
from app import app
from app.models.place_book import PlaceBook
from app.models.place import Place
from app.models.user import User
from return_styles import ListStyle
from index import type_test

''' Import packages '''
from flask_json import as_json, request
from flask import abort
from datetime import datetime, timedelta
import json

@app.route('/places/<place_id>/books', methods=['GET'])
@as_json
def get_place_bookings(place_id):
    """
    Get all bookings
    List all bookings for a place in the database.
    ---
    tags:
        - PlaceBook
    parameters:
        -
            name: place_id
            in: path
            type: integer
            required: True
            description: ID of the place
    responses:
        200:
            description: List of all bookings
            schema:
                id: Bookings
                required:
                    - data
                    - paging
                properties:
                    data:
                        type: array
                        description: bookings array
                        items:
                            $ref: '#/definitions/get_booking_get_Booking'
                    paging:
                        description: pagination
                        schema:
                            $ref: '#/definitions/get_amenities_get_Paging'
    """
    try:
        ''' Check if place_id exists '''
        query = Place.select().where(Place.id == place_id)
        if not query.exists():
            raise LookupError('place_id')

        ''' Return list of bookings for the given place '''
        data = PlaceBook.select().where(PlaceBook.place == place_id)
        return ListStyle.list(data, request), 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        abort(500)

@app.route('/places/<place_id>/books', methods=['POST'])
@as_json
def book_date(place_id):
    """
    Create a new booking
    Create a new booking for the given place
    ---
    tags:
        - PlaceBook
    parameters:
        -
            name: place_id
            in: path
            type: integer
            required: True
            description: ID of the place
        -
            name: user_id
            in: form
            type: integer
            required: True
            description: ID of the booking user
        -
            name: is_validated
            in: form
            type: boolean
            description: Defines if the booking is validated
        -
            name: date_start
            in: form
            type: string
            required: True
            description: Date the booking begins
        -
            name: number_nights
            in: form
            type: integer
            description: Number of nights of the booking
    responses:
        201:
            description: Booking was created
            schema:
                $ref: '#/definitions/create_amenity_post_post_success'
        400:
            description: Issue with booking request
        404:
            description: Place was not found
        410:
            description: Place is unavailable for the requested booking
        500:
            description: The request was not able to be processed
    """
    data = {}
    for key in request.form.keys():
    	for value in request.form.getlist(key):
    		data[key] = value
    try:
        ''' Check if place_id exists '''
        query = Place.select().where(Place.id == place_id)
        if not query.exists():
            raise LookupError('place_id')

        ''' Check if required keys are included '''
        if not 'user_id' in data:
            raise KeyError('user_id')
        elif not 'date_start' in data:
            raise KeyError('date_start')

        ''' Check if user_id is an integer '''
        if not type_test(data['user_id'], int):
            raise TypeError('user_id is not an integer')

        ''' Check if user_id exists '''
        query = User.select().where(User.id == data['user_id'])
        if not query.exists():
            raise LookupError('user_id')

        ''' Check if date_start is a string '''
        if not type_test(data['date_start'], 'string'):
            raise TypeError('date_start is not a string')

        ''' Check if date_start string if formatted correctly '''
        if not datetime.strptime(data['date_start'], "%Y/%m/%d %H:%M:%S"):
            raise ValueError('date_start is not formatted correctly')

        ''' Check if is_validated is a boolean '''
        if 'is_validated' in data:
            if not type_test(data['is_validated'], bool):
                raise TypeError('is_validated is not a boolean')

        ''' Check if number_nights is an integer '''
        if 'number_nights' in data:
            if not type_test(data['number_nights'], int):
                raise TypeError('number_nights is not an integer')

        ''' Check if place is already booked '''
        book_start = datetime.strptime(data['date_start'], "%Y/%m/%d %H:%M:%S").replace(hour=0, minute=0, second=0)
        book_end = book_start + timedelta(days= int(data['number_nights']))
        bookings = PlaceBook.select().where(PlaceBook.place == place_id)
        for booking in bookings:
            date_start = booking.date_start.replace(hour=0, minute=0, second=0)
            date_end = date_start + timedelta(days= int(booking.number_nights))
            if book_start >= date_start and book_start < date_end:
                raise ValueError('booked')
            elif book_end > date_start and book_end <= date_end:
                raise ValueError('booked')
            elif date_start >= book_start and date_start < book_end:
                raise ValueError('booked')

        ''' Create new booking '''
        new = PlaceBook(
            place = place_id,
            user = data['user_id'],
            date_start = datetime.strptime(data['date_start'], "%Y/%m/%d %H:%M:%S")
        )
        if 'is_validated' in data:
            new.is_validated = data['is_validated']
        if 'number_nights' in data:
            new.number_nights = data['number_nights']
        new.save()
        res = {}
        res['code'] = 201
        res['id'] = new.id
        res['msg'] = "Booking of place was created successfully"
        return res, 201
    except KeyError as e:
        res = {}
        res['code'] = 40000
        res['msg'] = 'Missing parameters'
        return res, 400
    except LookupError as e:
        abort(404)
    except ValueError as e:
        if e.message == 'booked':
            res = {}
            res['code'] = 110000
            res['msg'] = 'Place unavailable at this date'
            return res, 410
        res = {}
        res['code'] = 400
        res['msg'] = e.message
        return res, 400
    except TypeError as e:
        res = {}
        res['code'] = 400
        res['msg'] = e.message
        return res, 400
    except Exception as e:
        print e.message
        abort(500)

@app.route('/places/<place_id>/books/<book_id>', methods=['GET'])
@as_json
def get_booking(place_id, book_id):
    """
    Get the given booking
    Return the given booking in the database.
    ---
    tags:
        - PlaceBook
    parameters:
        -
            in: path
            name: place_id
            type: integer
            required: True
            description: ID of the place
        -
            in: path
            name: book_id
            type: integer
            required: True
            description: ID of the booking
    responses:
        200:
            description: Booking returned successfully
            schema:
                id: Booking
                required:
                    - place_id
                    - user_id
                    - date_start
                    - id
                    - created_at
                    - updated_at
                properties:
                    place_id:
                        type: integer
                        description: ID of the place
                        default: 1
                    user_id:
                        type: number
                        description: id of the state
                        default: 1
                    is_validated:
                        type: boolean
                        description: defines if the booking is validated
                        default: False
                    date_start:
                        type: string
                        description: the start date of the booking
                        default: '2016-08-11 20:30:38'
                    number_nights:
                        type: integer
                        description: the number of nights of the booking
                        default: 1
                    id:
                        type: number
                        description: id of the booking
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
            description: Place or booking was not found
        500:
            description: Request could not be processed
    """
    try:
        ''' Test if place does not exist '''
        query = Place.select().where(Place.id == place_id)
        if not query.exists():
            raise LookupError('place_id')

        ''' Test if booking does not exist '''
        query = PlaceBook.select().where(PlaceBook.id == book_id)
        if not query.exists():
            raise LookupError('bookd_id')

        ''' Check if place, booking combo exists '''
        query = query.where(PlaceBook.place == place_id)
        if not query.exists():
            raise LookupError('book_id, place_id')

        ''' Return booking data '''
        booking = PlaceBook.get(PlaceBook.id == book_id, PlaceBook.place == place_id)
        return booking.to_dict(), 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        abort(500)

@app.route('/places/<place_id>/books/<book_id>', methods=['PUT'])
@as_json
def update_booking(place_id, book_id):
    """
    Update a booking
    Update a booking for the given place
    ---
    tags:
        - PlaceBook
    parameters:
        -
            name: place_id
            in: path
            type: integer
            required: True
            description: ID of the place
        -
            name: book_id
            in: path
            type: integer
            required: True
            description: ID of the booking
        -
            name: is_validated
            in: form
            type: boolean
            description: Defines if the booking is validated
        -
            name: date_start
            in: form
            type: string
            description: Date the booking begins
        -
            name: number_nights
            in: form
            type: integer
            description: Number of nights of the booking
    responses:
        200:
            description: Booking was updated
            schema:
                id: put_success
                required:
                    - code
                    - id
                    - msg
                properties:
                    code:
                        type: integer
                        description: Response code from the API
                        default: 200
                    msg:
                        type: string
                        description: Message about record creation
                        default: "updated successfully"
        400:
            description: Issue with booking update request
        404:
            description: Place was not found
        410:
            description: Place is unavailable for the requested booking
        500:
            description: The request was not able to be processed
    """
    data = {}
    for key in request.form.keys():
        for value in request.form.getlist(key):
        	data[key] = value
    try:
        ''' Test if place does not exist '''
        query = Place.select().where(Place.id == place_id)
        if not query.exists():
            raise LookupError('place_id')

        ''' Test if booking does not exist '''
        query = PlaceBook.select().where(PlaceBook.id == book_id)
        if not query.exists():
            raise LookupError('book_id')

        ''' Check if place, booking combo exists '''
        query = PlaceBook.select().where(PlaceBook.id == book_id, PlaceBook.place == place_id)
        if not query.exists():
            raise LookupError('book_id, place_id')

        ''' Check if user_id in data '''
        if 'user_id' in data:
            raise ValueError('User cannot be changed')

        ''' Get the record for update '''
        booking = PlaceBook.get(PlaceBook.id == book_id, PlaceBook.place == place_id)

        ''' Check if is_validated in data '''
        if 'is_validated' in data:
            if not type_test(data['is_validated'], bool):
                raise TypeError("Value of 'is_validated' should be a boolean")
            if data['is_validated'] == 'True':
                booking.is_validated = True
            else:
                booking.is_validated = False

        ''' Check if date_start in data '''
        if 'date_start' in data:
            if not type_test(data['date_start'], 'string'):
                raise TypeError("Value of 'date_start' should be a string")
            if not datetime.strptime(data['date_start'], "%Y/%m/%d %H:%M:%S"):
                raise TypeError("'date_start' is not formatted properly")
            booking.date_start = data['date_start']

        ''' Check if number_nights in data '''
        if 'number_nights' in data:
            if not type_test(data['number_nights'], int):
                raise TypeError("Value of 'number_nights' should be a integer")
            booking.number_nights = data['number_nights']
        booking.save()
        res = {}
        res['code'] = 200
        res['msg'] = "Booking of place was updated successfully"
        return res, 200
    except LookupError as e:
        abort(404)
    except TypeError as e:
        res = {}
        res['code'] = 400
        res['msg'] = e.message
        return res, 400
    except ValueError as e:
        if e.message == 'User cannot be changed':
            res = {}
            res['code'] = 403
            res['msg'] = e.message
            return res, 403
        res = {}
        res['code'] = 400
        res['msg'] = e.message
        return res, 400
    except Exception as e:
        abort(500)

@app.route('/places/<place_id>/books/<book_id>', methods=['DELETE'])
@as_json
def delete_booking(place_id, book_id):
    """
    Delete the given booking
    Deletes the given booking in the database.
    ---
    tags:
        - PlaceBook
    parameters:
        -
            in: path
            name: place_id
            type: integer
            required: True
            description: ID of the place
        -
            in: path
            name: book_id
            type: integer
            required: True
            description: ID of the booking
    responses:
        200:
            description: Booking deleted successfully
            schema:
                $ref: '#/definitions/delete_amenity_delete_delete_200'
        404:
            description: Booking was not found
        500:
            description: Request could not be processed
    """
    try:
        ''' Test if place does not exist '''
        query = Place.select().where(Place.id == place_id)
        if not query.exists():
            raise LookupError('place_id')

        ''' Test if booking does not exist '''
        query = PlaceBook.select().where(PlaceBook.id == book_id)
        if not query.exists():
            raise LookupError('book_id')

        ''' Check if place, booking combo exists '''
        query = query.where(PlaceBook.place == place_id)
        if not query.exists():
            raise LookupError('book_id, place_id')

        ''' Delete the given booking '''
        booking = PlaceBook.delete().where(PlaceBook.id == book_id, PlaceBook.place == place_id)
        booking.execute()
        res = {}
        res['code'] = 200
        res['msg'] = "Booking was deleted successfully"
        return res, 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        abort(500)

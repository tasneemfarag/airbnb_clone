''' Import app and models '''
from app import app
from app.models.place_book import PlaceBook
from app.models.place import Place
from app.models.user import User

''' Import packages '''
from flask_json import as_json, request
from flask import abort
from datetime import datetime, timedelta
import json

@app.route('/places/<place_id>/books', methods=['GET'])
@as_json
def get_place_bookings(place_id):
    ''' Gets all bookings for a given place '''
    try:
        ''' Check if place_id exists '''
        query = Place.select().where(Place.id == place_id)
        if not query.exists():
            raise LookupError('place_id')

        ''' Return list of bookings for the given place '''
        booked_dates = []
        data = PlaceBook.select().where(PlaceBook.place == place_id)
        for row in data:
            booked_dates.append(row.to_dict())
        return {"result": booked_dates}, 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        abort(500)

@app.route('/places/<place_id>/books', methods=['POST'])
@as_json
def book_date(place_id):
    ''' Creates a new booking for a place '''
    data = json.loads(request.data)
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
        if not isinstance(data['user_id'], int):
            raise TypeError('user_id is not an integer')

        ''' Check if user_id exists '''
        query = User.select().where(User.id == data['user_id'])
        if not query.exists():
            raise LookupError('user_id')

        ''' Check if date_start is a string '''
        if not isinstance(data['date_start'], unicode):
            raise TypeError('date_start is not a string')

        ''' Check if date_start string if formatted correctly '''
        if not datetime.strptime(data['date_start'], "%Y/%m/%d %H:%M:%S"):
            raise ValueError('date_start is not formatted correctly')

        ''' Check if is_validated is a boolean '''
        if 'is_validated' in data:
            if not isinstance(data['is_validated'], bool):
                raise TypeError('is_validated is not a boolean')

        ''' Check if number_nights is an integer '''
        if 'number_nights' in data:
            if not isinstance(data['number_nights'], int):
                raise TypeError('number_nights is not an integer')

        ''' Check if place is already booked '''
        book_start = datetime.strptime(data['date_start'], "%Y/%m/%d %H:%M:%S").replace(hour=0, minute=0, second=0)
        book_end = book_start + timedelta(days= data['number_nights'])
        bookings = PlaceBook.select().where(PlaceBook.place == place_id)
        for booking in bookings:
            date_start = booking.date_start.replace(hour=0, minute=0, second=0)
            date_end = date_start + timedelta(days= booking.number_nights)
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
    ''' Returns the given booking's details '''
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
    ''' Updates the given bookings information '''
    data = json.loads(request.data)
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
            if not isinstance(data['is_validated'], bool):
                raise TypeError("Value of 'is_validated' should be a boolean")
            booking.is_validated = data['is_validated']

        ''' Check if date_start in data '''
        if 'date_start' in data:
            if not isinstance(data['date_start'], unicode):
                raise TypeError("Value of 'date_start' should be a string")
            if not datetime.strptime(data['date_start'], "%Y/%m/%d %H:%M:%S"):
                raise TypeError("'date_start' is not formatted properly")
            booking.date_start = data['date_start']

        ''' Check if number_nights in data '''
        if 'number_nights' in data:
            if not isinstance(data['number_nights'], int):
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
    ''' Deletes the given booking '''
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

from app.models.place_book import PlaceBook
from app.models.place import Place
from app.models.user import User
from flask_json import as_json, request
from flask import abort
from app import app
from datetime import datetime
import json
from peewee import IntegrityError

@app.route('/places/<place_id>/books', methods=['GET'])
@as_json
def get_place_bookings(place_id):
    ''' Gets all bookings for a given place '''
    try:
        booked_dates = []
        data = PlaceBook.select().where(PlaceBook.place == place_id)
        for row in data:
            booked_dates.append(row.to_hash())
        return {"result": booked_dates}, 200
    except Exception as error:
        if "Instance matching query does not exist" in error.message:
            abort(404)

@app.route('/places/<place_id>/books', methods=['POST'])
@as_json
def book_date(place_id):
    ''' Creates a new booking for a place '''
    try:
        data = json.loads(request.data)
        new = PlaceBook(
            place = place_id,
            user = data['user_id'],
            date_start = datetime.strptime(data['date_start'], "%Y/%m/%d %H:%M:%S")
        )
        if 'is_validated' in data:
            if not isinstance(data['is_validated'], bool):
                raise IntegrityError
            new.is_validated = data['is_validated']
        if 'number_nights' in data:
            if not isinstance(data['number_nights'], int):
                raise IntegrityError
            new.number_nights = data['number_nights']
        new.save()
        res = {}
        res['code'] = 201
        res['id'] = new.id
        res['msg'] = "Booking of place was created successfully"
        return res, 201
    except KeyError as error:
        res = {}
        res['code'] = 400
        res['msg'] = str(error.message) + ' is missing'
        return res, 400
    except ValueError as error:
        res = {}
        res['code'] = 400
        res['msg'] = error.message
        return res, 400
    except Exception as error:
        if "Instance matching query does not exist" in error.message:
            abort(404)
        elif type(error).__name__ == 'IntegrityError':
            res = {}
            res['code'] = 400
            res['msg'] = 'The data provided is invalid'
            return res, 400
        else:
            print error
            print type(error)
            print type(error).__name__
            return {}, 500

@app.route('/places/<place_id>/books/<book_id>', methods=['GET'])
@as_json
def get_booking(place_id, book_id):
    ''' Returns the given booking's details '''
    try:
        booking = PlaceBook.get(PlaceBook.id == book_id)
        return booking.to_hash(), 200
    except Exception as error:
        if "Instance matching query does not exist" in error.message:
            abort(404)
        else:
            print error
            print type(error)
            print type(error).__name__
            return {}, 500

@app.route('/places/<place_id>/books/<book_id>', methods=['PUT'])
@as_json
def update_booking(place_id, book_id):
    ''' Updates the given bookings information '''
    try:
        booking = PlaceBook.get(PlaceBook.id == book_id)
        data = json.loads(request.data)
        for key in data:
            if key == 'user_id':
                raise Exception('User cannot be changed')
            elif key == 'is_validated':
                booking.is_validated = data[key]
            elif key == 'date_start':
                booking.date_start = datetime.strptime(data[key], "%Y/%m/%d %H:%M:%S")
            elif key == 'number_nights':
                booking.number_nights = data[key]
        booking.save()
        res = {}
        res['code'] = 200
        res['msg'] = "Booking of place was updated successfully"
        return res, 200
    except Exception as error:
        if "Instance matching query does not exist" in error.message:
            abort(404)
        else:
            res = {}
            res['code'] = 403
            res['msg'] = str(error)
            return res, 403

@app.route('/places/<place_id>/books/<book_id>', methods=['DELETE'])
@as_json
def delete_booking(place_id, book_id):
    ''' Deletes the given booking '''
    try:
        booking = PlaceBook.delete().where(PlaceBook.id == book_id)
        booking.execute()
        response = {}
        response['code'] = 200
        response['msg'] = "Booking was deleted"
        return response, 200
    except Exception as error:
        if "Instance matching query does not exist" in error.message:
            abort(404)
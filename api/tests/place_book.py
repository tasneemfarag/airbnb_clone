''' Import app and models '''
from app import app
from app.models.base import db
from app.models.place_book import PlaceBook
from app.models.place import Place
from app.models.user import User
from app.models.state import State
from app.models.city import City

''' Import test data '''
from user_data import good_user_1, good_user_2
from state_data import good_state_1
from city_data import good_city_1
from place_data import good_place_1, good_place_2
from place_book_data import *

''' Import packages '''
import unittest
import json
import logging

class AppTestCase(unittest.TestCase):

    def setUp(self):
        db.connect()
        db.create_tables([User, State, City, PlaceBook, Place])
        logging.disable(logging.CRITICAL)
        self.app = app.test_client()

    def tearDown(self):
        db.drop_tables([User, State, City, PlaceBook, Place])
        db.close()

    def test_create(self):
        ''' Set base data '''
        rv = self.app.post('/users', data=good_user_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', data=good_user_2)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states', data=good_state_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', data=good_city_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/places', data=good_place_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/places', data=good_place_2)
        self.assertEqual(rv.status_code, 201)

        ''' Test if place does not exist '''
        rv = self.app.post('/places/404/books', data=good_place_book_1)
        self.assertEqual(rv.status_code, 404)

        ''' Create new bookings '''
        rv = self.app.post('/places/1/books', data=good_place_book_1)
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data['id'], 1)

        rv = self.app.post('/places/2/books', data=good_place_book_2)
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data['id'], 2)

        ''' Test if user does not exist '''
        rv = self.app.post('/places/1/books', data=bad_place_book_1)
        self.assertEqual(rv.status_code, 404)

        ''' Test if user_id is missing '''
        rv = self.app.post('/places/1/books', data=bad_place_book_2)
        self.assertEqual(rv.status_code, 400)

        ''' Test if date_start is missing '''
        rv = self.app.post('/places/1/books', data=bad_place_book_3)
        self.assertEqual(rv.status_code, 400)

        ''' Test if user_id type is invalid '''
        rv = self.app.post('/places/1/books', data=bad_place_book_4)
        self.assertEqual(rv.status_code, 400)

        ''' Test if is_validated type is invalid '''
        rv = self.app.post('/places/1/books', data=bad_place_book_5)
        self.assertEqual(rv.status_code, 400)

        ''' Test if date_start type is invalid '''
        rv = self.app.post('/places/1/books', data=bad_place_book_6)
        self.assertEqual(rv.status_code, 400)

        ''' Test if date_start string formatted incorrectly '''
        rv = self.app.post('/places/1/books', data=bad_place_book_7)
        self.assertEqual(rv.status_code, 400)

        ''' Test if number_nights type is invalid '''
        rv = self.app.post('/places/1/books', data=bad_place_book_8)
        self.assertEqual(rv.status_code, 400)

        ''' Test if already booked and starts during booking'''
        rv = self.app.post('/places/1/books', data=bad_place_book_9)
        self.assertEqual(rv.status_code, 410)

        ''' Test if already booked and ends during booking '''
        rv = self.app.post('/places/1/books', data=bad_place_book_10)
        self.assertEqual(rv.status_code, 410)

        ''' Test if already booked and surrounds booking '''
        rv = self.app.post('/places/1/books', data=bad_place_book_11)
        self.assertEqual(rv.status_code, 410)

    def test_list(self):
        ''' Set base data '''
        rv = self.app.post('/users', data=good_user_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', data=good_user_2)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states', data=good_state_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', data=good_city_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/places', data=good_place_1)
        self.assertEqual(rv.status_code, 201)

        ''' Test if place does not exist '''
        rv = self.app.get('/places/404/books')
        self.assertEqual(rv.status_code, 404)

        ''' Confirm no bookings exist '''
        rv = self.app.get('/places/1/books')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['data']
        self.assertEqual(len(data), 0)

        ''' Create new booking '''
        rv = self.app.post('/places/1/books', data=good_place_book_1)
        self.assertEqual(rv.status_code, 201)

        ''' Confirm one booking exists '''
        rv = self.app.get('/places/1/books')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['data']
        self.assertEqual(len(data), 1)

    def test_get(self):
        ''' Set base data '''
        rv = self.app.post('/users', data=good_user_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', data=good_user_2)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states', data=good_state_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', data=good_city_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/places', data=good_place_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/places/1/books', data=good_place_book_1)
        self.assertEqual(rv.status_code, 201)

        ''' Test if place does not exist '''
        rv = self.app.get('/places/404/books/1')
        self.assertEqual(rv.status_code, 404)

        ''' Test if booking does not exist '''
        rv = self.app.get('/places/1/books/404')
        self.assertEqual(rv.status_code, 404)

        ''' Retrieve created booking and confirm data '''
        rv = self.app.get('/places/1/books/1')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertEqual(data['user_id'], good_place_book_1['user_id'])

    def test_delete(self):
        ''' Set base data '''
        rv = self.app.post('/users', data=good_user_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', data=good_user_2)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states', data=good_state_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', data=good_city_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/places', data=good_place_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/places/1/books', data=good_place_book_1)
        self.assertEqual(rv.status_code, 201)

        ''' Test if place does not exist '''
        rv = self.app.delete('/places/404/books/1')
        self.assertEqual(rv.status_code, 404)

        ''' Test if booking does not exist '''
        rv = self.app.delete('/places/1/books/404')
        self.assertEqual(rv.status_code, 404)

        ''' Confirm that there is one booking '''
        rv = self.app.get('/places/1/books')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['data']
        self.assertEqual(len(data), 1)

        ''' Delete the existing booking '''
        booking = self.app.delete('/places/1/books/1')

        ''' Confirm that no bookings exist '''
        rv = self.app.get('/places/1/books')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['data']
        self.assertEqual(len(data), 0)

    def test_update(self):
        ''' Set base data '''
        rv = self.app.post('/users', data=good_user_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', data=good_user_2)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states', data=good_state_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', data=good_city_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/places', data=good_place_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/places', data=good_place_2)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/places/1/books', data=good_place_book_1)
        self.assertEqual(rv.status_code, 201)

        ''' Test if place does not exist '''
        rv = self.app.delete('/places/404/books/1', data={})
        self.assertEqual(rv.status_code, 404)

        ''' Test if booking does not exist '''
        rv = self.app.delete('/places/1/books/404', data={})
        self.assertEqual(rv.status_code, 404)

        ''' Test if place, booking combo does not exist '''
        rv = self.app.delete('/places/2/books/1', data={})
        self.assertEqual(rv.status_code, 404)

        ''' Test if attempting to update the 'user_id' '''
        rv = self.app.put('/places/1/books/1', data={'user_id': 2})
        self.assertEqual(rv.status_code, 403)

        ''' Test if is_validated is an invalid type '''
        rv = self.app.put('/places/1/books/1', data={'is_validated': 400})
        self.assertEqual(rv.status_code, 400)

        ''' Test if date_start is an invalid type '''
        rv = self.app.put('/places/1/books/1', data={'date_start': 400})
        self.assertEqual(rv.status_code, 400)

        ''' Test if date_start is not formatted correctly '''
        rv = self.app.put('/places/1/books/1', data={'date_start': '07/24/1984'})
        self.assertEqual(rv.status_code, 400)

        ''' Test if number_nights is an invalid type '''
        rv = self.app.put('/places/1/books/1', data={'number_nights': 'Nope'})
        self.assertEqual(rv.status_code, 400)

        ''' Test updating is_validated '''
        rv = self.app.put('/places/1/books/1', data={'is_validated': True})
        self.assertEqual(rv.status_code, 200)

        ''' Test updating data_start '''
        rv = self.app.put('/places/1/books/1', data={'date_start': datetime.now().strftime("%Y/%m/%d %H:%M:%S")})
        self.assertEqual(rv.status_code, 200)

        ''' Test updating number_nights '''
        rv = self.app.put('/places/1/books/1', data={'number_nights': 20})
        self.assertEqual(rv.status_code, 200)

        '''Check that updates were processed '''
        rv = self.app.get('/places/1/books/1')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertEqual(data['user_id'], good_place_book_1['user_id'])
        self.assertNotEqual(data['is_validated'], good_place_book_1['is_validated'])
        self.assertNotEqual(data['date_start'], good_place_book_1['date_start'])
        self.assertNotEqual(data['number_nights'], good_place_book_1['number_nights'])

if __name__ == '__main__':
    unittest.main()

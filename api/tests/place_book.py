from app import app
from app.models.base import db
from app.models.place_book import PlaceBook
from app.models.place import Place
from app.models.user import User
from app.models.state import State
from app.models.city import City
import unittest
import json
import logging
from user_data import good_user_1, good_user_2
from state_data import good_state_1
from city_data import good_city_1
from place_book_data import *
from place_data import good_place_1, good_place_2

class AppTestCase(unittest.TestCase):

    def setUp(self):
        db.connect()
        db.create_tables([User, State, City, PlaceBook, Place])
        logging.disable(logging.CRITICAL)
        self.app = app.test_client()

    def tearDown(self):
        db.drop_tables([User, State, City, PlaceBook, Place])
        db.close()

    # def test_create(self):
    #     ''' Set base data '''
    #     rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_2))
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_1))
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_2))
    #     self.assertEqual(rv.status_code, 201)
    #
    #     ''' create correctly a booking if all required parameters are send '''
    #     rv = self.app.post('/places/1/books', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_book_1))
    #     self.assertEqual(rv.status_code, 201)
    #     data = json.loads(rv.data)
    #     self.assertEqual(data['id'], 1)
    #     rv = self.app.post('/places/2/books', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_book_2))
    #     self.assertEqual(rv.status_code, 201)
    #     data = json.loads(rv.data)
    #     self.assertEqual(data['id'], 2)
    #
    #     ''' test all cases of missing parameters '''
    #     rv = self.app.post('/places/1/books', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_book_2))
    #     self.assertEqual(rv.status_code, 400)
    #     rv = self.app.post('/places/1/books', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_book_4))
    #     self.assertEqual(rv.status_code, 400)
    #     rv = self.app.post('/places/1/books', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_book_7))
    #     self.assertEqual(rv.status_code, 400)
    #     rv = self.app.post('/places/1/books', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_book_8))
    #     self.assertEqual(rv.status_code, 400)
    #     rv = self.app.post('/places/1/books', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_book_9))
    #     self.assertEqual(rv.status_code, 400)
    #     rv = self.app.post('/places/1/books', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_book_10))
    #     self.assertEqual(rv.status_code, 400)

    # def test_list(self):
    #     ''' Set base data '''
    #     rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_2))
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_1))
    #     self.assertEqual(rv.status_code, 201)
    #
    #     ''' return 0 elements if no booking was created'''
    #     rv = self.app.get('/places/1/books')
    #     self.assertEqual(rv.status_code, 200)
    #     data = json.loads(rv.data)['result']
    #     self.assertEqual(len(data), 0)
    #
    #     ''' return 1 element after a booking creation'''
    #     self.app.post('/places/1/books', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_book_1))
    #     rv = self.app.get('/places/1/books')
    #     self.assertEqual(rv.status_code, 200)
    #     data = json.loads(rv.data)['result']
    #     self.assertEqual(len(data), 1)
    #
    # def test_get(self):
    #     ''' Set base data '''
    #     rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_2))
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_1))
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.app.post('/places/1/books', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_book_1))
    #
    #     ''' create a booking and after get it '''
    #     rv = self.app.get('/places/1/books/1')
    #
    #     ''' check the status code '''
    #     self.assertEqual(rv.status_code, 200)
    #
    #     ''' check if it's the same resource as during the creation '''
    #     booking = json.loads(rv.data)
    #     self.assertEqual(booking['user_id'], good_place_book_1['user_id'])
    #
    #     ''' check when trying to get an unknown booking '''
    #     rv = self.app.get('/places/1/books/500')
    #     self.assertEqual(rv.status_code, 404)
    #
    # def test_delete(self):
    #     ''' Set base data '''
    #     rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_2))
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_1))
    #     self.assertEqual(rv.status_code, 201)
    #     rv = self.app.post('/places/1/books', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_book_1))
    #
    #     ''' create a booking and after delete it '''
    #     before = len(json.loads(self.app.get('/places/1/books').data)['result'])
    #     rv = self.app.delete('/places/1/books/1')
    #     after = len(json.loads(self.app.get('/places/1/books').data)['result'])
    #
    #     ''' check the status code '''
    #     self.assertEqual(rv.status_code, 200)
    #
    #     ''' check the number of element before and after a delete '''
    #     self.assertEqual(after - before, -1)

    def test_update(self):
        ''' Set base data '''
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_2))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_2))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/places/1/books', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_book_1))

        '''create a booking and after update it'''
        test2 = self.app.put('/places/1/books/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'user_id': 2}))
        test3 = self.app.put('/places/1/books/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'is_validated': True}))
        test4 = self.app.put('/places/1/books/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'date_start': datetime.now().strftime("%Y/%m/%d %H:%M:%S")}))
        test5 = self.app.put('/places/1/books/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'number_nights': 20}))

        '''check the status code'''
        self.assertEqual(test2.status_code, 403)
        self.assertEqual(test3.status_code, 200)
        self.assertEqual(test4.status_code, 200)
        self.assertEqual(test5.status_code, 200)

        '''check the impact of each request parameters'''
        rv = self.app.get('/places/1/books/1')
        booking = json.loads(rv.data)
        self.assertEqual(booking['user_id'], good_place_book_1['user_id'])
        self.assertNotEqual(booking['is_validated'], good_place_book_1['is_validated'])
        self.assertNotEqual(booking['date_start'], good_place_book_1['date_start'])
        self.assertNotEqual(booking['number_nights'], good_place_book_1['number_nights'])

        '''check when trying to update an unknown booking '''
        rv = self.app.put('/places/1/books/200', {'number_nights': 25})
        self.assertEqual(rv.status_code, 404)

if __name__ == '__main__':
    unittest.main()

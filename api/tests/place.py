from app import app
from app.models.base import db
from app.models.place import Place
from app.models.user import User
from app.models.state import State
from app.models.city import City
import unittest
import json
import logging
from place_data import *
from user_data import *
from state_data import *
from city_data import *

class AppTestCase(unittest.TestCase):

    def setUp(self):
        db.connect()
        db.create_tables([Place, User, State, City])
        logging.disable(logging.CRITICAL)
        self.app = app.test_client()

    def tearDown(self):
        db.drop_tables([Place, User, State, City])
        db.close()

    def test_create(self):
        ''' Set base data '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
        self.assertEqual(rv.status_code, 201)

        ''' create correctly a place if all required parameters are sent '''
        rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_1))
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data['id'], 1)
        rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_2))
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data['id'], 2)

        ''' test all cases of missing parameters '''
        rv = self.app.post('places', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_1))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_2))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_3))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_4))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_5))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_6))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_7))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_8))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_9))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_10))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_11))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_12))
        self.assertEqual(rv.status_code, 400)

    def test_list(self):
        ''' Set base data '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
        self.assertEqual(rv.status_code, 201)

        ''' return 0 elements if no place was created'''
        rv = self.app.get('/places')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['result']
        self.assertEqual(len(data), 0)

        ''' return 1 element after a place creation'''
        rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_1))
        rv = self.app.get('/places')
        data = json.loads(rv.data)['result']
        self.assertEqual(len(data), 1)

    def test_get(self):
        ''' Set base data '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
        self.assertEqual(rv.status_code, 201)

        ''' create a place and after get it '''
        rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_1))
        rv = self.app.get('/places/1')

        ''' check the status code '''
        self.assertEqual(rv.status_code, 200)

        ''' check if it's the same resource as during the creation '''
        place = json.loads(rv.data)
        self.assertEqual(place['name'], good_place_1['name'])

        ''' check when trying to get an unknown place '''
        rv = self.app.get('/places/500')
        self.assertEqual(rv.status_code, 404)

    def test_delete(self):
        ''' Set base data '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
        self.assertEqual(rv.status_code, 201)

        ''' create a city and after delete it '''
        rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_1))
        before = len(json.loads(self.app.get('/places').data)['result'])
        rv = self.app.delete('/places/1')
        after = len(json.loads(self.app.get('/places').data)['result'])

        ''' check the status code '''
        self.assertEqual(rv.status_code, 200)

        ''' check the number of element before and after a delete '''
        self.assertEqual(after - before, -1)

    def test_update(self):
        ''' Set base data '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
        self.assertEqual(rv.status_code, 201)

        '''create a place and after update it'''
        rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_1))
        test1 = self.app.put('/places/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'owner_id': 20}))
        test2 = self.app.put('/places/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'city_id': 20}))
        test3 = self.app.put('/places/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'name': 'This is the next best place after the other'}))
        test4 = self.app.put('/places/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'description': 'There is no describing this place'}))
        test5 = self.app.put('/places/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'number_rooms': 8}))
        test6 = self.app.put('/places/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'number_bathrooms': 5}))
        test7 = self.app.put('/places/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'max_guest': 10}))
        test8 = self.app.put('/places/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'price_by_night': 125}))
        test9 = self.app.put('/places/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'latitude': 32.83838}))
        test10 = self.app.put('/places/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'longitude': -100.12345}))

        '''check the status code'''
        self.assertEqual(test1.status_code, 403)
        self.assertEqual(test2.status_code, 403)
        self.assertEqual(test3.status_code, 200)
        self.assertEqual(test4.status_code, 200)
        self.assertEqual(test5.status_code, 200)
        self.assertEqual(test6.status_code, 200)
        self.assertEqual(test7.status_code, 200)
        self.assertEqual(test8.status_code, 200)
        self.assertEqual(test9.status_code, 200)
        self.assertEqual(test10.status_code, 200)

        '''check the impact of each request parameters'''
        rv = self.app.get('/places/1')
        place = json.loads(rv.data)
        self.assertEqual(place['owner_id'], good_place_1['owner_id'])
        self.assertEqual(place['city_id'], good_place_1['city_id'])
        self.assertNotEqual(place['name'], good_place_1['name'])
        self.assertNotEqual(place['description'], good_place_1['description'])
        self.assertNotEqual(place['number_rooms'], good_place_1['number_rooms'])
        self.assertNotEqual(place['number_bathrooms'], good_place_1['number_bathrooms'])
        self.assertNotEqual(place['max_guest'], good_place_1['max_guest'])
        self.assertNotEqual(place['price_by_night'], good_place_1['price_by_night'])
        self.assertNotEqual(place['latitude'], good_place_1['latitude'])
        self.assertNotEqual(place['longitude'], good_place_1['longitude'])

        '''check when trying to update an unknown user (user ID not linked to a user)'''
        rv = self.app.put('/places/200', headers={'Content-Type': 'application/json'}, data=json.dumps({'name': 'Supers Awesome Locale'}))
        self.assertEqual(rv.status_code, 404)

    def test_create_by_city(self):
        ''' Set base data '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
        self.assertEqual(rv.status_code, 201)

        ''' create correctly a place by city if all required parameters are sent '''
        rv = self.app.post('/states/1/cities/1/places', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_by_city_1))
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data['id'], 1)
        rv = self.app.post('/states/1/cities/1/places', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_by_city_2))
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data['id'], 2)

        ''' test all cases of missing parameters '''
        rv = self.app.post('/states/1/cities/1/places', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_1))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/states/1/cities/1/places', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_3))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/states/1/cities/1/places', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_4))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/states/1/cities/1/places', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_5))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/states/1/cities/1/places', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_6))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/states/1/cities/1/places', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_7))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/states/1/cities/1/places', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_8))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/states/1/cities/1/places', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_9))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/states/1/cities/1/places', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_10))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/states/1/cities/1/places', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_place_11))
        self.assertEqual(rv.status_code, 400)

    def test_list_by_city(self):
        ''' Set base data '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
        self.assertEqual(rv.status_code, 201)

        ''' return 0 elements if no place was created'''
        rv = self.app.get('/states/1/cities/1/places')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['result']
        self.assertEqual(len(data), 0)

        ''' return 1 element after a place creation'''
        rv = self.app.post('/states/1/cities/1/places', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_1))
        rv = self.app.get('/states/1/cities/1/places')
        data = json.loads(rv.data)['result']
        self.assertEqual(len(data), 1)

if __name__ == '__main__':
    unittest.main()

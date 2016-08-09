''' Import app and models '''
from app import app
from app.models.base import db
from app.models.city import City
from app.models.state import State

''' Import test data '''
from city_data import *
from state_data import *

''' Import packages '''
import unittest
import json
import logging

class AppTestCase(unittest.TestCase):

    def setUp(self):
        db.connect()
        db.create_tables([City, State])
        logging.disable(logging.CRITICAL)
        self.app = app.test_client()

    def tearDown(self):
        db.drop_tables([City, State])
        db.close()

    def test_create(self):
        '''Set base data'''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        self.assertEqual(rv.status_code, 201)

        ''' Test creation of cities in the given state '''
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data['id'], 1)

        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_2))
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data['id'], 2)

        ''' Test if 'name' value is NULL '''
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_city_1))
        self.assertEqual(rv.status_code, 400)

        ''' Test if 'name' value is not a string '''
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_city_2))
        self.assertEqual(rv.status_code, 400)

        ''' Test if 'name' key is not in data '''
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_city_3))
        self.assertEqual(rv.status_code, 400)

        ''' Test if state does not exist '''
        rv = self.app.post('/states/404/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
        self.assertEqual(rv.status_code, 404)

        ''' Test if city already exists '''
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
        self.assertEqual(rv.status_code, 409)

    def test_list(self):
        ''' Set base data '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        self.assertEqual(rv.status_code, 201)

        ''' Test if state does not exist '''
        rv = self.app.get('/states/404/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
        self.assertEqual(rv.status_code, 404)

        ''' Test that no cities exist '''
        rv = self.app.get('/states/1/cities')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['result']
        self.assertEqual(len(data), 0)

        ''' Create a new city '''
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
        self.assertEqual(rv.status_code, 201)

        ''' return 1 element after a state creation'''
        rv = self.app.get('/states/1/cities')
        data = json.loads(rv.data)['result']
        self.assertEqual(len(data), 1)

    def test_get(self):
        ''' Set base data '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
        self.assertEqual(rv.status_code, 201)

        ''' Test if state does not exist '''
        rv = self.app.get('/states/404/cities/1')
        self.assertEqual(rv.status_code, 404)

        ''' Test if city does not exist '''
        rv = self.app.get('/states/1/cities/404')
        self.assertEqual(rv.status_code, 404)

        ''' Retrieve the newly created city '''
        rv = self.app.get('/states/1/cities/1')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertEqual(data['name'], good_city_1['name'])

    def test_delete(self):
        ''' Set base data '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
        self.assertEqual(rv.status_code, 201)

        ''' Test if state does not exist '''
        rv = self.app.delete('/states/404/cities/1')
        self.assertEqual(rv.status_code, 404)

        ''' Test if city does not exist '''
        rv = self.app.delete('/states/1/cities/404')
        self.assertEqual(rv.status_code, 404)

        ''' Check the a city exists '''
        rv = self.app.get('/states/1/cities')
        data = json.loads(rv.data)['result']
        self.assertEqual(len(data), 1)

        ''' Delete the existing city '''
        rv = self.app.delete('/states/1/cities/1')
        self.assertEqual(rv.status_code, 200)

        ''' Check that the city was deleted '''
        rv = self.app.get('/states/1/cities')
        data = json.loads(rv.data)['result']
        self.assertEqual(len(data), 0)

if __name__ == '__main__':
    unittest.main()

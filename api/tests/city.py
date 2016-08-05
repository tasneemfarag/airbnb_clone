from app import app
from app.models.base import db
from app.models.city import City
from app.models.state import State
import unittest
import json
import logging
from city_data import *
from state_data import *

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
        ''' create correctly a city if all required parameters are send '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data['id'], 1)
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_2))
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data['id'], 2)

        ''' test all cases of missing parameters '''
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_city_1))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_city_2))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_city_3))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/states/500/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
        self.assertEqual(rv.status_code, 404)

    def test_list(self):
        ''' return 0 elements if no city was created'''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        rv = self.app.get('/states/1/cities')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['result']
        self.assertEqual(len(data), 0)

        ''' return 1 element after a state creation'''
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
        rv = self.app.get('/states/1/cities')
        data = json.loads(rv.data)['result']
        self.assertEqual(len(data), 1)

    def test_get(self):
        ''' create a city and after get it '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
        rv = self.app.get('/states/1/cities/1')

        ''' check the status code '''
        self.assertEqual(rv.status_code, 200)

        ''' check if it's the same resource as during the creation '''
        city = json.loads(rv.data)
        self.assertEqual(city['name'], good_city_1['name'])

        ''' check when trying to get an unknown city '''
        rv = self.app.get('/states/1/cities/500')
        self.assertEqual(rv.status_code, 404)

    def test_delete(self):
        ''' create a city and after delete it '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
        before = len(json.loads(self.app.get('/states/1/cities').data)['result'])
        rv = self.app.delete('/states/1/cities/1')
        after = len(json.loads(self.app.get('/states/1/cities').data)['result'])

        ''' check the status code '''
        self.assertEqual(rv.status_code, 200)

        ''' check the number of element before and after a delete '''
        self.assertEqual(after - before, -1)

if __name__ == '__main__':
    unittest.main()

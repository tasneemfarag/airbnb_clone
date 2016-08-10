''' Import app and models '''
from app import app
from app.models.base import db
from app.models.state import State

''' Import test data '''
from state_data import *

''' Import packages '''
import unittest
import json
import logging

class AppTestCase(unittest.TestCase):

    def setUp(self):
        db.connect()
        db.create_tables([State], safe=True)
        logging.disable(logging.CRITICAL)
        self.app = app.test_client()

    def tearDown(self):
        db.drop_tables([State])
        db.close()

    def test_create(self):
        ''' Test the create with valid data '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data['id'], 1)
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_2))
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data['id'], 2)

        ''' Test if state is NULL '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_state_1))
        self.assertEqual(rv.status_code, 400)

        ''' Test if name  value type is invalid '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_state_2))
        self.assertEqual(rv.status_code, 400)

        ''' Test if name key is missing '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_state_3))
        self.assertEqual(rv.status_code, 400)

        ''' Test that two states cannot be the same name '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        rv = self.assertEqual(rv.status_code, 409)

    def test_list(self):
        ''' Test that there are no states returned '''
        rv = self.app.get('/states')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['result']
        self.assertEqual(len(data), 0)

        ''' Create a new state '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        self.assertEqual(rv.status_code, 201)

        ''' Test that there is one state returned '''
        rv = self.app.get('/states')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['result']
        self.assertEqual(len(data), 1)

    def test_get(self):
        ''' Set base data '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        self.assertEqual(rv.status_code, 201)

        ''' Test if state doesn't exist '''
        rv = self.app.get('/states/404')
        self.assertEqual(rv.status_code, 404)

        ''' Retrieve the newly created state '''
        rv = self.app.get('/states/1')
        self.assertEqual(rv.status_code, 200)

        ''' Confirm retrieved state is the created state '''
        data = json.loads(rv.data)
        self.assertEqual(data['name'], good_state_1['name'])

    def test_delete(self):
        ''' Set base data '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        self.assertEqual(rv.status_code, 201)

        ''' Test if state doesn't exist '''
        rv = self.app.delete('/states/404')
        self.assertEqual(rv.status_code, 404)

        ''' Test that one state exists '''
        rv = self.app.get('/states')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['result']
        self.assertEqual(len(data), 1)

        ''' Delete the existing state '''
        rv = self.app.delete('/states/1')
        self.assertEqual(rv.status_code, 200)

        ''' Test that there are no states '''
        rv = self.app.get('/states')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['result']
        self.assertEqual(len(data), 0)

if __name__ == '__main__':
    unittest.main()

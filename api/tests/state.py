from app import app
from app.models.base import db
from app.models.state import State
import unittest
import json
import logging
from state_data import *

class AppTestCase(unittest.TestCase):

    def setUp(self):
        db.connect()
        db.create_tables([State])
        logging.disable(logging.CRITICAL)
        self.app = app.test_client()

    def tearDown(self):
        db.drop_tables([State])
        db.close()

    def test_create(self):
        ''' create correctly a state if all required parameters are send '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data['id'], 1)
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_2))
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data['id'], 2)

        ''' test all cases of missing parameters '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_state_1))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_state_2))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_state_3))
        self.assertEqual(rv.status_code, 400)

        ''' check if a state can't have the same email '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        rv = self.assertEqual(rv.status_code, 409)

    def test_list(self):
        ''' return 0 elements if no state was created'''
        rv = self.app.get('/states')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['result']
        self.assertEqual(len(data), 0)

        ''' return 1 element after a state creation'''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        rv = self.app.get('/states')
        data = json.loads(rv.data)['result']
        self.assertEqual(len(data), 1)

    def test_get(self):
        ''' create a state and after get it '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        rv = self.app.get('/states/1')

        ''' check the status code '''
        self.assertEqual(rv.status_code, 200)

        ''' check if it's the same resource as during the creation '''
        state = json.loads(rv.data)
        self.assertEqual(state['name'], good_state_1['name'])

        ''' check when trying to get an unknown state '''
        rv = self.app.get('/states/500')
        self.assertEqual(rv.status_code, 404)

    def test_delete(self):
        ''' create a state and after delete it '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        before = len(json.loads(self.app.get('/states').data)['result'])
        rv = self.app.delete('/states/1')
        after = len(json.loads(self.app.get('/states').data)['result'])

        ''' check the status code '''
        self.assertEqual(rv.status_code, 200)

        ''' check the number of element before and after a delete '''
        self.assertEqual(after - before, -1)

        ''' check when trying to delete an unknown state '''
        rv = self.app.delete('/states/500')
        self.assertEqual(rv.status_code, 200)

if __name__ == '__main__':
    unittest.main()

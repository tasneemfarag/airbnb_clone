''' Import app and models '''
from app import app
from app.models.base import db
from app.models.user import User

''' Import test data '''
from user_data import *

''' Import packages '''
from datetime import datetime
import unittest
import json
import logging

class AppTestCase(unittest.TestCase):

    def setUp(self):
        db.connect()
        db.create_tables([User], safe=True)
        logging.disable(logging.CRITICAL)
        self.app = app.test_client()

    def tearDown(self):
        db.drop_tables([User])
        db.close()

    def test_create(self):
        ''' Test the creation of a new user '''
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data['id'], 1)

        ''' Test for missing email '''
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_user_1))
        self.assertEqual(rv.status_code, 400)

        ''' Test for missing first_name '''
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_user_2))
        self.assertEqual(rv.status_code, 400)

        ''' Test for missing last_name '''
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_user_3))
        self.assertEqual(rv.status_code, 400)

        ''' Test for missing password '''
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_user_4))
        self.assertEqual(rv.status_code, 400)

        ''' Test for invalid email '''
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_user_5))
        self.assertEqual(rv.status_code, 400)

        ''' Test for invalid first_name '''
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_user_6))
        self.assertEqual(rv.status_code, 400)

        ''' Test for invalid last_name '''
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_user_7))
        self.assertEqual(rv.status_code, 400)

        ''' Test for invalid is_admin '''
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_user_8))
        self.assertEqual(rv.status_code, 400)

        ''' Test for invalid password '''
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_user_9))
        self.assertEqual(rv.status_code, 400)

        ''' Test if user already exists '''
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
        rv = self.assertEqual(rv.status_code, 409)

    def test_list(self):
        ''' Test that no users exist '''
        rv = self.app.get('/users')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertEqual(len(data['result']), 0)

        ''' Create a new user '''
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
        self.assertEqual(rv.status_code, 201)

        ''' Test that one user exists '''
        rv = self.app.get('/users')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['result']
        self.assertEqual(len(data), 1)

    def test_get(self):
        ''' Set base data '''
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
        self.assertEqual(rv.status_code, 201)

        ''' Test if user does not exist '''
        rv = self.app.get('/users/404')
        self.assertEqual(rv.status_code, 404)

        ''' Retrieve newly created user '''
        rv = self.app.get('/users/1')
        self.assertEqual(rv.status_code, 200)

        ''' Test that the user is same as created '''
        user = json.loads(rv.data)
        self.assertEqual(user['email'], good_user_1['email'])

    def test_delete(self):
        ''' Set base data '''
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
        self.assertEqual(rv.status_code, 201)

        ''' Test that one user exists '''
        rv = self.app.get('/users')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['result']
        self.assertEqual(len(data), 1)

        ''' Delete the existing user '''
        rv = self.app.delete('/users/1')
        self.assertEqual(rv.status_code, 200)

        ''' Test that no users exist '''
        rv = self.app.get('/users')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['result']
        self.assertEqual(len(data), 0)

        ''' Test delete if the user does not exist '''
        rv = self.app.delete('/users/404')
        self.assertEqual(rv.status_code, 404)

    def test_update(self):
        ''' Set base data '''
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
        self.assertEqual(rv.status_code, 201)

        ''' Test that email cannot be updated '''
        rv = self.app.put('/users/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'email': 'update@superawesome.com'}))
        self.assertEqual(rv.status_code, 403)

        ''' Test updating first_name '''
        rv = self.app.put('/users/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'first_name': 'Change'}))
        self.assertEqual(rv.status_code, 200)

        ''' Test updating last_name '''
        rv = self.app.put('/users/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'last_name': 'User'}))
        self.assertEqual(rv.status_code, 200)

        ''' Test updating is_admin '''
        rv = self.app.put('/users/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'is_admin': False}))
        self.assertEqual(rv.status_code, 200)

        ''' Test updating password '''
        rv = self.app.put('/users/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'password': 'notthesame'}))
        self.assertEqual(rv.status_code, 200)

        ''' Test for invalid first_name '''
        rv = self.app.put('/users/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'first_name': 400}))
        self.assertEqual(rv.status_code, 400)

        ''' Test for invalid last_name '''
        rv = self.app.put('/users/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'last_name': 400}))
        self.assertEqual(rv.status_code, 400)

        ''' Test for invalid is_admin '''
        rv = self.app.put('/users/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'is_admin': 'Nope'}))
        self.assertEqual(rv.status_code, 400)

        ''' Test for invalid password '''
        rv = self.app.put('/users/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'password': 400}))
        self.assertEqual(rv.status_code, 400)

        ''' Test that expected updates occurred '''
        rv = self.app.get('/users/1')
        self.assertEqual(rv.status_code, 200)
        user = json.loads(rv.data)
        self.assertEqual(user['email'], good_user_1['email'])
        self.assertNotEqual(user['first_name'], good_user_1['first_name'])
        self.assertNotEqual(user['last_name'], good_user_1['last_name'])
        self.assertNotEqual(user['is_admin'], good_user_1['is_admin'])

        ''' Test if user does not exist '''
        rv = self.app.put('/users/404', headers={'Content-Type': 'application/json'}, data=json.dumps({'first_name': 'Change'}))
        self.assertEqual(rv.status_code, 404)

if __name__ == '__main__':
    unittest.main()

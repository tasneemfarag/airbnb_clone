from app import app
from app.models.base import db
from app.models.user import User
import unittest
from datetime import datetime
import json
import logging
from user_data import *

class AppTestCase(unittest.TestCase):

    def setUp(self):
        db.connect()
        if User.table_exists():
            db.drop_tables([User])
        db.create_tables([User])
        logging.disable(logging.CRITICAL)
        self.app = app.test_client()

    def tearDown(self):
        db.drop_tables([User])
        db.close()

    def test_create(self):
        ''' create correctly a user if all required parameters are send '''
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
        data = json.loads(rv.data)
        self.assertEqual(rv.status_code, 201)
        self.assertEqual(data['id'], 1)
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_2))
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data['id'], 2)

        ''' test all cases of missing parameters '''
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_user_1))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_user_2))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_user_3))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_user_4))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_user_5))
        self.assertEqual(rv.status_code, 400)

        ''' check if an user can't have the same email '''
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
        rv = self.assertEqual(rv.status_code, 409)

    def test_list(self):
        ''' return 0 elements if no user was created'''
        rv = self.app.get('/users')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertEqual(len(data['result']), 0)

        ''' return 1 element after a user creation'''
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.get('/users')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['result']
        self.assertEqual(len(data), 1)

    def test_get(self):
        ''' create a user and after get it '''
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.get('/users')

        ''' check the status code '''
        self.assertEqual(rv.status_code, 200)

        ''' check if it's the same resource as during the creation '''
        user = json.loads(rv.data)['result'][0]
        self.assertEqual(user['email'], good_user_1['email'])

        ''' check when trying to get an unknown user (user ID not linked to a user)'''
        rv = self.app.get('/users/4')
        self.assertEqual(rv.status_code, 404)

    def test_delete(self):
        ''' create a user and after delete it '''
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
        before = len(json.loads(self.app.get('/users').data)['result'])
        rv = self.app.delete('/users/1')
        after = len(json.loads(self.app.get('/users').data)['result'])

        ''' check the status code '''
        self.assertEqual(rv.status_code, 200)

        ''' check the number of element before and after a delete '''
        self.assertEqual(after - before, -1)

        ''' check when trying to delete an unknown user (user ID not linked to a user) '''
        rv = self.app.delete('/users/200')
        self.assertEqual(rv.status_code, 200)
        rv = self.app.get('/users')
        data = json.loads(rv.data)
        self.assertEqual(len(data['result']), 0)

    def test_update(self):
        '''create a user and after update it'''
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
        test1 = self.app.put('/users/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'email': 'update@superawesome.com'}))
        test2 = self.app.put('/users/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'first_name': 'Change'}))
        test3 = self.app.put('/users/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'last_name': 'User'}))
        test4 = self.app.put('/users/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'is_admin': False}))
        test5 = self.app.put('/users/1', headers={'Content-Type': 'application/json'}, data=json.dumps({'password': 'notthesame'}))

        '''check the status code'''
        self.assertEqual(test1.status_code, 400)
        self.assertEqual(test2.status_code, 200)
        self.assertEqual(test3.status_code, 200)
        self.assertEqual(test4.status_code, 200)
        self.assertEqual(test5.status_code, 200)

        '''check the impact of each request parameters'''
        rv = self.app.get('/users/1')
        user = json.loads(rv.data)
        self.assertEqual(user['email'], good_user_1['email'])
        self.assertNotEqual(user['first_name'], good_user_1['first_name'])
        self.assertNotEqual(user['last_name'], good_user_1['last_name'])
        self.assertNotEqual(user['is_admin'], good_user_1['is_admin'])

        '''check when trying to update an unknown user (user ID not linked to a user)'''
        rv = self.app.put('/users/200', headers={'Content-Type': 'application/json'}, data=json.dumps({'first_name': 'Change'}))
        self.assertEqual(rv.status_code, 404)

if __name__ == '__main__':
    unittest.main()

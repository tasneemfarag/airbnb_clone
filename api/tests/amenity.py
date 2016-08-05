from app import app
from app.models.base import db
from app.models.amenity import Amenity
import unittest
import json
import logging
from amenity_data import *

class AppTestCase(unittest.TestCase):

    def setUp(self):
        db.connect()
        db.create_tables([Amenity])
        logging.disable(logging.CRITICAL)
        self.app = app.test_client()

    def tearDown(self):
        db.drop_tables([Amenity])
        db.close()

    def test_create(self):
        ''' create correctly an amenity if all required parameters are send '''
        rv = self.app.post('/amenities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_amenity_1))
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data['id'], 1)
        rv = self.app.post('/amenities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_amenity_2))
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data['id'], 2)

        ''' test all cases of missing parameters '''
        rv = self.app.post('/amenities', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_amenity_1))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/amenities', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_amenity_2))
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/amenities', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_amenity_3))
        self.assertEqual(rv.status_code, 400)

    def test_list(self):
        ''' return 0 elements if no amenity was created'''
        rv = self.app.get('/amenities')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['result']
        self.assertEqual(len(data), 0)

        ''' return 1 element after an amenity creation'''
        rv = self.app.post('/amenities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_amenity_1))
        rv = self.app.get('/amenities')
        data = json.loads(rv.data)['result']
        self.assertEqual(len(data), 1)

    def test_get(self):
        ''' create an amenity and after get it '''
        rv = self.app.post('/amenities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_amenity_1))
        rv = self.app.get('/amenities/1')

        ''' check the status code '''
        self.assertEqual(rv.status_code, 200)

        ''' check if it's the same resource as during the creation '''
        amenity = json.loads(rv.data)
        self.assertEqual(amenity['name'], good_amenity_1['name'])

        ''' check when trying to get an unknown amenity '''
        rv = self.app.get('/amenities/500')
        self.assertEqual(rv.status_code, 404)

    def test_delete(self):
        ''' create an amenity and after delete it '''
        rv = self.app.post('/amenities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_amenity_1))
        rv = self.app.get('/amenities')
        before = len(json.loads(self.app.get('/amenities').data)['result'])
        rv = self.app.delete('/amenities/1')
        rv = self.app.get('/amenities')
        after = len(json.loads(self.app.get('/amenities').data)['result'])

        ''' check the status code '''
        self.assertEqual(rv.status_code, 200)

        ''' check the number of element before and after a delete '''
        self.assertEqual(after - before, -1)

if __name__ == '__main__':
    unittest.main()

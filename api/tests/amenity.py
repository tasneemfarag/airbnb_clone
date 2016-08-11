''' Import app and models '''
from app import app
from app.models.base import db
from app.models.state import State
from app.models.city import City
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.place_amenity import PlaceAmenities

''' Import test data '''
from state_data import good_state_1
from city_data import good_city_1
from user_data import good_user_1
from place_data import good_place_1
from amenity_data import *

''' Import packages '''
import unittest
import json
import logging

class AppTestCase(unittest.TestCase):

    def setUp(self):
        db.connect()
        db.create_tables([State, City, User, Place, Amenity, PlaceAmenities], safe=True)
        logging.disable(logging.CRITICAL)
        self.app = app.test_client()

    def tearDown(self):
        db.drop_tables([State, City, User, Place, Amenity, PlaceAmenities])
        db.close()

    def test_create(self):
        ''' Test creation of new amenities '''
        rv = self.app.post('/amenities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_amenity_1))
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data['id'], 1)

        rv = self.app.post('/amenities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_amenity_2))
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data['id'], 2)

        ''' Test if name is NULL '''
        rv = self.app.post('/amenities', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_amenity_1))
        self.assertEqual(rv.status_code, 400)

        ''' Test if name is not string type '''
        rv = self.app.post('/amenities', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_amenity_2))
        self.assertEqual(rv.status_code, 400)

        ''' Test if key 'name' is missing '''
        rv = self.app.post('/amenities', headers={'Content-Type': 'application/json'}, data=json.dumps(bad_amenity_3))
        self.assertEqual(rv.status_code, 400)

    def test_list(self):
        ''' Check if no amenities '''
        rv = self.app.get('/amenities')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['data']
        self.assertEqual(len(data), 0)

        ''' Create new amenity '''
        rv = self.app.post('/amenities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_amenity_1))
        self.assertEqual(rv.status_code, 201)

        ''' Check if one amenity '''
        rv = self.app.get('/amenities')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['data']
        self.assertEqual(len(data), 1)

    def test_get(self):
        ''' Set base data '''
        rv = self.app.post('/amenities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_amenity_1))
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data['id'], 1)

        ''' Retrieve the newly created amenity '''
        rv = self.app.get('/amenities/1')
        self.assertEqual(rv.status_code, 200)

        ''' Test if amenity is the created amenity '''
        amenity = json.loads(rv.data)
        self.assertEqual(amenity['name'], good_amenity_1['name'])

        ''' Test if amenity does not exist '''
        rv = self.app.get('/amenities/404')
        self.assertEqual(rv.status_code, 404)

    def test_delete(self):
        ''' Set base data '''
        rv = self.app.post('/amenities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_amenity_1))
        self.assertEqual(rv.status_code, 201)

        ''' Test if amenity does not exist '''
        rv = self.app.delete('/amenities/404')
        self.assertEqual(rv.status_code, 404)

        ''' Test number of amenities before delete '''
        rv = self.app.get('/amenities')
        data = json.loads(rv.data)['data']
        self.assertEqual(len(data), 1)

        ''' Delete the existing amenity '''
        rv = self.app.delete('/amenities/1')
        self.assertEqual(rv.status_code, 200)

        ''' Test number of amenities after delete '''
        rv = self.app.get('/amenities')
        data = json.loads(rv.data)['data']
        self.assertEqual(len(data), 0)

    def test_create_place_amenity(self):
        ''' Set base data '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/amenities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_amenity_1))
        self.assertEqual(rv.status_code, 201)

        ''' Test if place does not exist '''
        rv = self.app.post('/places/404/amenities/1')
        self.assertEqual(rv.status_code, 404)

        ''' Test if amenity does not exist '''
        rv = self.app.post('/places/1/amenities/404')
        self.assertEqual(rv.status_code, 404)

        ''' Create new amenity for place '''
        rv = self.app.post('/places/1/amenities/1')
        self.assertEqual(rv.status_code, 201)

        ''' Test error if place, amenity combo exists '''
        rv = self.app.post('/places/1/amenities/1')
        self.assertEqual(rv.status_code, 400)

    def test_get_place_amenities(self):
        ''' Set base data '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/amenities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_amenity_1))
        self.assertEqual(rv.status_code, 201)

        ''' Test if place does not exist '''
        rv = self.app.get('/places/404/amentities')
        self.assertEqual(rv.status_code, 404)

        ''' Confirm there are no place amenities '''
        rv = self.app.get('/places/1/amenities')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['data']
        self.assertEqual(len(data), 0)

        ''' Create new amenity for place '''
        rv = self.app.post('/places/1/amenities/1')
        self.assertEqual(rv.status_code, 201)

        ''' Confirm there is one place amenity '''
        rv = self.app.get('/places/1/amenities')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['data']
        self.assertEqual(len(data), 1)

    def test_delete_place_amenity(self):
        ''' Set base data '''
        rv = self.app.post('/states', headers={'Content-Type': 'application/json'}, data=json.dumps(good_state_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_city_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', headers={'Content-Type': 'application/json'}, data=json.dumps(good_user_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/places', headers={'Content-Type': 'application/json'}, data=json.dumps(good_place_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/amenities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_amenity_1))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/amenities', headers={'Content-Type': 'application/json'}, data=json.dumps(good_amenity_2))
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/places/1/amenities/1')
        self.assertEqual(rv.status_code, 201)

        ''' Test if place does not exist '''
        rv = self.app.delete('/places/404/amenities/1')
        self.assertEqual(rv.status_code, 404)

        ''' Test if amenity does not exist '''
        rv = self.app.delete('/places/1/amenities/404')
        self.assertEqual(rv.status_code, 404)

        ''' Test if place, amenity combo does not exist '''
        rv = self.app.delete('/places/1/amenities/2')
        self.assertEqual(rv.status_code, 404)

        ''' Test deletion of place amenity '''
        rv = self.app.get('/places/1/amenities')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['data']
        self.assertEqual(len(data), 1)

        rv = self.app.delete('/places/1/amenities/1')
        self.assertEqual(rv.status_code, 200)

        rv = self.app.get('/places/1/amenities')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['data']
        self.assertEqual(len(data), 0)

if __name__ == '__main__':
    unittest.main()

''' Import app and models '''
from app import app
from app.models.base import db
from app.models.place import Place
from app.models.user import User
from app.models.state import State
from app.models.city import City
from app.models.place_book import PlaceBook

''' Import test data '''
from place_data import *
from user_data import *
from state_data import *
from city_data import *
from place_book import good_place_book_1

''' Import packages '''
from datetime import datetime, timedelta
import unittest
import json
import logging


class AppTestCase(unittest.TestCase):

    def setUp(self):
        db.connect()
        db.create_tables([Place, User, State, City, PlaceBook])
        logging.disable(logging.CRITICAL)
        self.app = app.test_client()

    def tearDown(self):
        db.drop_tables([Place, User, State, City, PlaceBook])
        db.close()

    def test_create(self):
        ''' Set base data '''
        rv = self.app.post('/states', data=good_state_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', data=good_city_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', data=good_user_1)
        self.assertEqual(rv.status_code, 201)

        ''' Test creation of places '''
        rv = self.app.post('/places', data=good_place_1)
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data['id'], 1)
        rv = self.app.post('/places', data=good_place_2)
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data['id'], 2)

        ''' Test if owner_id is missing '''
        rv = self.app.post('places', data=bad_place_1)
        self.assertEqual(rv.status_code, 400)

        ''' Test if city_id is missing '''
        rv = self.app.post('/places', data=bad_place_2)
        self.assertEqual(rv.status_code, 400)

        ''' Test if name is missing '''
        rv = self.app.post('/places', data=bad_place_3)
        self.assertEqual(rv.status_code, 400)

        ''' Test if owner_id is an invalid data type '''
        rv = self.app.post('/places', data=bad_place_4)
        self.assertEqual(rv.status_code, 400)

        ''' Test if city_id is an invalid data type '''
        rv = self.app.post('/places', data=bad_place_5)
        self.assertEqual(rv.status_code, 400)

        ''' Test if name is an invalid data type '''
        rv = self.app.post('/places', data=bad_place_6)
        self.assertEqual(rv.status_code, 400)

        ''' Test if description is an invalid data type '''
        rv = self.app.post('/places', data=bad_place_7)
        self.assertEqual(rv.status_code, 400)

        ''' Test if number_rooms is an invalid data type '''
        rv = self.app.post('/places', data=bad_place_8)
        self.assertEqual(rv.status_code, 400)

        ''' Test if number_bathrooms is an invalid data type '''
        rv = self.app.post('/places', data=bad_place_9)
        self.assertEqual(rv.status_code, 400)

        ''' Test if max_guest is an invalid data type '''
        rv = self.app.post('/places', data=bad_place_10)
        self.assertEqual(rv.status_code, 400)

        ''' Test if price_by_night is an invalid data type '''
        rv = self.app.post('/places', data=bad_place_11)
        self.assertEqual(rv.status_code, 400)

        ''' Test if latitude is an invalid data type '''
        rv = self.app.post('/places', data=bad_place_12)
        self.assertEqual(rv.status_code, 400)

        ''' Test if longitude is an invalid data type '''
        rv = self.app.post('/places', data=bad_place_13)
        self.assertEqual(rv.status_code, 400)

        ''' Test if owner_id does not exist '''
        rv = self.app.post('/places', data=bad_place_14)
        self.assertEqual(rv.status_code, 404)

        ''' Test if city_id does not exist '''
        rv = self.app.post('/places', data=bad_place_15)
        self.assertEqual(rv.status_code, 404)

    def test_list(self):
        ''' Set base data '''
        rv = self.app.post('/states', data=good_state_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', data=good_city_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', data=good_user_1)
        self.assertEqual(rv.status_code, 201)

        ''' Test that there are currently no places '''
        rv = self.app.get('/places')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['data']
        self.assertEqual(len(data), 0)

        ''' Create a new place '''
        rv = self.app.post('/places', data=good_place_1)
        self.assertEqual(rv.status_code, 201)

        ''' Test that there is one place '''
        rv = self.app.get('/places')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['data']
        self.assertEqual(len(data), 1)

    def test_get(self):
        ''' Set base data '''
        rv = self.app.post('/states', data=good_state_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', data=good_city_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', data=good_user_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/places', data=good_place_1)
        self.assertEqual(rv.status_code, 201)

        ''' Test if place_id does not exist '''
        rv = self.app.get('/places/404')
        self.assertEqual(rv.status_code, 404)

        ''' Retrieve the newly created place '''
        rv = self.app.get('/places/1')
        self.assertEqual(rv.status_code, 200)

        ''' Test that data matches what was sent '''
        data = json.loads(rv.data)
        self.assertEqual(data['name'], good_place_1['name'])

    def test_delete(self):
        ''' Set base data '''
        rv = self.app.post('/states', data=good_state_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', data=good_city_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', data=good_user_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/places', data=good_place_1)
        self.assertEqual(rv.status_code, 201)

        ''' Test if place_id does not exist '''
        rv = self.app.delete('/places/404')
        self.assertEqual(rv.status_code, 404)

        ''' Test that one place exists '''
        rv = self.app.get('/places')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['data']
        self.assertEqual(len(data), 1)

        ''' Delete the existing place '''
        rv = self.app.delete('/places/1')
        self.assertEqual(rv.status_code, 200)

        ''' Test that no places exist '''
        rv = self.app.get('/places')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['data']
        self.assertEqual(len(data), 0)

    def test_update(self):
        ''' Set base data '''
        rv = self.app.post('/states', data=good_state_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', data=good_city_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', data=good_user_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/places', data=good_place_1)
        self.assertEqual(rv.status_code, 201)

        ''' Test if place_id does not exist '''
        rv = self.app.put('/places/404', data={'name': 'Super awesomeness!'})
        self.assertEqual(rv.status_code, 404)

        ''' Test updating protected values '''
        rv = self.app.put('/places/1', data={'owner_id': 20})
        self.assertEqual(rv.status_code, 403)
        rv = self.app.put('/places/1', data={'city_id': 20})
        self.assertEqual(rv.status_code, 403)

        ''' Test invalid data type updates '''
        rv = self.app.put('/places/1', data={'name': 400})
        self.assertEqual(rv.status_code, 400)
        rv = self.app.put('/places/1', data={'description': 400})
        self.assertEqual(rv.status_code, 400)
        rv = self.app.put('/places/1', data={'number_rooms': 'nope'})
        self.assertEqual(rv.status_code, 400)
        rv = self.app.put('/places/1', data={'number_bathrooms': 'nope'})
        self.assertEqual(rv.status_code, 400)
        rv = self.app.put('/places/1', data={'max_guest': 'nope'})
        self.assertEqual(rv.status_code, 400)
        rv = self.app.put('/places/1', data={'price_by_night': 'nope'})
        self.assertEqual(rv.status_code, 400)
        rv = self.app.put('/places/1', data={'latitude': 'nope'})
        self.assertEqual(rv.status_code, 400)
        rv = self.app.put('/places/1', data={'longitude': 'nope'})
        self.assertEqual(rv.status_code, 400)

        ''' Test valid data type updates '''
        rv = self.app.put('/places/1', data={'name': 'This is the next best place after the other'})
        self.assertEqual(rv.status_code, 200)
        rv = self.app.put('/places/1', data={'description': 'There is no describing this place'})
        self.assertEqual(rv.status_code, 200)
        rv = self.app.put('/places/1', data={'number_rooms': 8})
        self.assertEqual(rv.status_code, 200)
        rv = self.app.put('/places/1', data={'number_bathrooms': 5})
        self.assertEqual(rv.status_code, 200)
        rv = self.app.put('/places/1', data={'max_guest': 10})
        self.assertEqual(rv.status_code, 200)
        rv = self.app.put('/places/1', data={'price_by_night': 125})
        self.assertEqual(rv.status_code, 200)
        rv = self.app.put('/places/1', data={'latitude': 32.83838})
        self.assertEqual(rv.status_code, 200)
        rv = self.app.put('/places/1', data={'longitude': -100.12345})
        self.assertEqual(rv.status_code, 200)

        ''' Test that the values were updated as expected '''
        rv = self.app.get('/places/1')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertEqual(data['owner_id'], good_place_1['owner_id'])
        self.assertEqual(data['city_id'], good_place_1['city_id'])
        self.assertNotEqual(data['name'], good_place_1['name'])
        self.assertNotEqual(data['description'], good_place_1['description'])
        self.assertNotEqual(data['number_rooms'], good_place_1['number_rooms'])
        self.assertNotEqual(data['number_bathrooms'], good_place_1['number_bathrooms'])
        self.assertNotEqual(data['max_guest'], good_place_1['max_guest'])
        self.assertNotEqual(data['price_by_night'], good_place_1['price_by_night'])
        self.assertNotEqual(data['latitude'], good_place_1['latitude'])
        self.assertNotEqual(data['longitude'], good_place_1['longitude'])

    def test_create_by_city(self):
        ''' Set base data '''
        rv = self.app.post('/states', data=good_state_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states', data=good_state_2)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', data=good_city_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', data=good_user_1)
        self.assertEqual(rv.status_code, 201)

        ''' Test creating places by city '''
        rv = self.app.post('/states/1/cities/1/places', data=good_place_by_city_1)
        self.assertEqual(rv.status_code, 201)
        data = json.loads(rv.data)
        self.assertEqual(data['id'], 1)

        ''' Test if owner_id is missing '''
        rv = self.app.post('/states/1/cities/1/places', data=bad_place_1)
        self.assertEqual(rv.status_code, 400)

        ''' Test if name is missing '''
        rv = self.app.post('/states/1/cities/1/places', data=bad_place_3)
        self.assertEqual(rv.status_code, 400)

        ''' Test if owner_id is an invalid data type '''
        rv = self.app.post('/states/1/cities/1/places', data=bad_place_4)
        self.assertEqual(rv.status_code, 400)

        ''' Test if name is an invalid data type '''
        rv = self.app.post('/states/1/cities/1/places', data=bad_place_6)
        self.assertEqual(rv.status_code, 400)

        ''' Test if description is an invalid data type '''
        rv = self.app.post('/states/1/cities/1/places', data=bad_place_7)
        self.assertEqual(rv.status_code, 400)

        ''' Test if number_rooms is an invalid data type '''
        rv = self.app.post('/states/1/cities/1/places', data=bad_place_8)
        self.assertEqual(rv.status_code, 400)

        ''' Test if number_bathrooms is an invalid data type '''
        rv = self.app.post('/states/1/cities/1/places', data=bad_place_9)
        self.assertEqual(rv.status_code, 400)

        ''' Test if max_guest is an invalid data type '''
        rv = self.app.post('/states/1/cities/1/places', data=bad_place_10)
        self.assertEqual(rv.status_code, 400)

        ''' Test if price_by_night is an invalid data type '''
        rv = self.app.post('/states/1/cities/1/places', data=bad_place_11)
        self.assertEqual(rv.status_code, 400)

        ''' Test if latitude is an invalid data type '''
        rv = self.app.post('/states/1/cities/1/places', data=bad_place_12)
        self.assertEqual(rv.status_code, 400)

        ''' Test if longitude is an invalid data type '''
        rv = self.app.post('/states/1/cities/1/places', data=bad_place_13)
        self.assertEqual(rv.status_code, 400)

        ''' Test if owner_id does not exist '''
        rv = self.app.post('/states/1/cities/1/places', data=bad_place_14)
        self.assertEqual(rv.status_code, 404)

        ''' Test if state_id does not exist '''
        rv = self.app.post('/states/404/cities/1/places', data=good_place_by_city_2)
        self.assertEqual(rv.status_code, 404)

        ''' Test if city_id does not exist '''
        rv = self.app.post('/states/1/cities/404/places', data=good_place_by_city_2)
        self.assertEqual(rv.status_code, 404)

        ''' Test if city_id is not linked to state_id '''
        rv = self.app.post('/states/2/cities/1/places', data=good_place_by_city_2)
        self.assertEqual(rv.status_code, 404)

    def test_list_by_city(self):
        ''' Set base data '''
        rv = self.app.post('/states', data=good_state_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states', data=good_state_2)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', data=good_city_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', data=good_user_1)
        self.assertEqual(rv.status_code, 201)

        ''' Test that no places exist for city '''
        rv = self.app.get('/states/1/cities/1/places')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['data']
        self.assertEqual(len(data), 0)

        ''' Create new place in city '''
        rv = self.app.post('/states/1/cities/1/places', data=good_place_1)
        self.assertEqual(rv.status_code, 201)

        ''' Test that one place exists in the city '''
        rv = self.app.get('/states/1/cities/1/places')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['data']
        self.assertEqual(len(data), 1)

        ''' Test if state_id does not exist '''
        rv = self.app.get('/states/404/cities/1/places')
        self.assertEqual(rv.status_code, 404)

        ''' Test if city_id does not exist '''
        rv = self.app.get('/states/1/cities/404/places')
        self.assertEqual(rv.status_code, 404)

        ''' Test if city_id is not linked to state_id '''
        rv = self.app.get('/states/2/cities/1/places')
        self.assertEqual(rv.status_code, 404)

    def test_list_by_state(self):
        ''' Set base data '''
        rv = self.app.post('/states', data=good_state_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states', data=good_state_2)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', data=good_city_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', data=good_user_1)
        self.assertEqual(rv.status_code, 201)

        ''' Test if state does not exist '''
        rv = self.app.get('/states/404/places')
        self.assertEqual(rv.status_code, 404)

        ''' Test if state has no cities '''
        rv = self.app.get('/states/2/places')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['data']
        self.assertEqual(len(data), 0)

        ''' Test if state has no places '''
        rv = self.app.get('/states/1/places')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['data']
        self.assertEqual(len(data), 0)

        ''' Create new place in city '''
        rv = self.app.post('/states/1/cities/1/places', data=good_place_1)
        self.assertEqual(rv.status_code, 201)

        ''' Test that new place is returned by state '''
        rv = self.app.get('/states/1/places')
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)['data']
        self.assertEqual(len(data), 1)

    def test_place_availability(self):
        ''' Set base data '''
        rv = self.app.post('/users', data=good_user_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/users', data=good_user_2)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states', data=good_state_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/states/1/cities', data=good_city_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/places', data=good_place_1)
        self.assertEqual(rv.status_code, 201)
        rv = self.app.post('/places/1/books', data=good_place_book_1)
        self.assertEqual(rv.status_code, 201)

        ''' Set booking test dates '''
        now = datetime.now()
        future = datetime.now() + timedelta(days=20)

        ''' Test missing required values '''
        rv = self.app.post('/places/1/available', data={'month': now.month, 'day': now.day})
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/places/1/available', data={'year': now.year, 'day': now.day})
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/places/1/available', data={'year': now.year, 'month': now.month})
        self.assertEqual(rv.status_code, 400)

        ''' Test invalid value types '''
        rv = self.app.post('/places/1/available', data={'year': 'nope', 'month': now.month, 'day': now.day})
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/places/1/available', data={'year': now.year, 'month': 'nope', 'day': now.day})
        self.assertEqual(rv.status_code, 400)
        rv = self.app.post('/places/1/available', data={'year': now.year, 'month': now.month, 'day': 'nope'})
        self.assertEqual(rv.status_code, 400)

        ''' Test if place does not exist '''
        rv = self.app.post('/places/404/available', data={'year': now.year, 'month': now.month, 'day': now.day})
        self.assertEqual(rv.status_code, 404)

        ''' Test booked date '''
        rv = self.app.post('/places/1/available', data={'year': now.year, 'month': now.month, 'day': now.day})
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertEqual(data['available'], False)

        ''' Test if date is not in a booked range '''
        rv = self.app.post('/places/1/available', data={'year': future.year, 'month': future.month, 'day': future.day})
        self.assertEqual(rv.status_code, 200)
        data = json.loads(rv.data)
        self.assertEqual(data['available'], True)



if __name__ == '__main__':
    unittest.main()

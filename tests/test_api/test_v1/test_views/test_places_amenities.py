#!/usr/bin/python3
import json
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity
from os import getenv
import requests
import unittest


host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', '5000')
version = '/v1'
api_url = 'http://{}:{}/api{}'.format(host, port, version)


WRONG_STATUS_CODE_MSG = 'Wrong status code!'
WRONG_TYPE_RETURN_MSG = 'Wrong return type return!'
WRONG_OBJ_TYPE_MSG = 'Wrong object type!'
MISSING_NAME_ATTR_MSG = 'Missing name!'
MISSING_CREATED_AT_ATTR_MSG = 'Missing created_at!'
MISSING_UPDATED_AT_ATTR_MSG = 'Missing updated_at!'
MISSING_CLASS_ATTR_MSG = 'Missing class!'
MISSING_STATE_ID_ATTR_MSG = 'Missing state id'


@unittest.skipIf(1, "not testing db storage")
class ListReviewsApiTest(unittest.TestCase):
    """
        Tests of API list action for Amenities linked to Places.
    """

    def setUp(self) -> None:
        """
            Set up API list action tests.
        """
        self.state = State(name='toto')
        self.state_id = self.state.id
        self.city = City(name='toto', state_id=self.state_id)
        self.city_id = self.city.id
        self.user = User(email='email', password='password')
        self.user_id = self.user.id
        self.place = Place(name='toto', city_id=self.city_id,
                           user_id=self.user_id)
        self.place_id = self.place.id
        storage.new(self.state)
        storage.new(self.city)
        storage.new(self.user)
        storage.new(self.place)
        storage.save()
        self.url = '{}/places/{}/amenities'.format(api_url, self.place_id)
        self.invalid_url = '{}/places/{}/amenities'.format(api_url, 'toto')

    def tearDown(self) -> None:
        """
            Tear down table Amenities linked to Places of
            database used for tests.
        """
        place = storage.get(Place, self.place_id)
        if place is not None:
            storage.delete(place)
        user = storage.get(User, self.user_id)
        if user is not None:
            storage.delete(user)
        city = storage.get(City, self.city_id)
        if city is not None:
            storage.delete(city)
        state = storage.get(State, self.state_id)
        if state is not None:
            storage.delete(state)
        storage.save()

    def testList(self):
        """
            Test valid list action.
        """
        response = requests.get(url=self.url)
        headers = response.headers

        self.assertEqual(response.status_code, 200, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)

    def testCount(self):
        """
            Test list length.
        """
        """
            Test list length.
        """
        user = User(email='email', password='password')
        amenity = Amenity(name='totoWifi')
        storage.new(user)
        storage.new(amenity)
        storage.save()
        obj_place = storage.get(Place, self.place_id)
        initial_count = len(obj_place.amenities)
        response = requests.get(url=self.url)
        json_data = response.json()

        self.assertEqual(initial_count, len(json_data))

        storage.delete(amenity)
        storage.delete(user)
        storage.save()

    def testOnlyAmenitiesInPlaces(self):
        """
            Test valid list action with Review content only.
        """
        user = User(email='email', password='password')
        amenity = Amenity(name='totoWifi')
        storage.new(amenity)
        storage.new(user)
        storage.save()
        response = requests.get(url=self.url)
        json_data = response.json()

        for element in json_data:
            self.assertEqual(element['__class__'],
                             'Review', WRONG_OBJ_TYPE_MSG)
        storage.delete(amenity)
        storage.delete(user)
        storage.save()

    def testNotFound(self):
        """
            Test create action when given wrong place_id or no ID at all.
        """
        response = requests.get(url=self.invalid_url)
        headers = response.headers
        json_data = response.json()

        self.assertEqual(response.status_code, 404, WRONG_STATUS_CODE_MSG)
        self.assertEqual(
            headers['Content-Type'], 'application/json', WRONG_TYPE_RETURN_MSG)
        self.assertTrue(self.place == storage.get(Place, self.place_id))
        self.assertIn('error', json_data)
        self.assertEqual(json_data['error'], 'Not found')

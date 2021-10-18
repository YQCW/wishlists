# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Pet API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN

  While debugging just these tests it's convinient to use this:
    nosetests --stop tests/test_service.py:TestPetServer
"""

import os
import logging
import unittest

# from unittest.mock import MagicMock, patch
from urllib.parse import quote_plus
from service import status  # HTTP Status Codes
from service.models import db, init_db,Wishlist, DataValidationError, db, Product
from service.routes import app
from .factories import WishlistFactory, ProductFactory



# Disable all but ciritcal errors during normal test run
# uncomment for debugging failing tests
logging.disable(logging.CRITICAL)

# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/wishlists"
CONTENT_TYPE_JSON = "application/json"


######################################################################
#  T E S T   C A S E S
######################################################################
class TestWishlistsServer(unittest.TestCase):
    """Wishlist Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # def _create_wishlists(self, count):
    #     """Factory method to create pets in bulk"""
    #     wishlists = []
    #     for _ in range(count):
    #         test_wishlist = WishlistFactory()
    #         resp = self.app.post(
    #             BASE_URL, json=test_wishlist.serialize(), content_type=CONTENT_TYPE_JSON
    #         )
    #         self.assertEqual(
    #             resp.status_code, status.HTTP_201_CREATED, "Could not create test wishlists"
    #         )
    #         new_wishlists = resp.get_json()
    #         test_wishlist.id = new_wishlists["id"]
    #         wishlists.append(test_pet)
    #     return wishlists

    def test_index(self):
        """Test the Home Page"""
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "Wishlist Demo REST API Service")

#     # def test_get_pet_list(self):
#     #     """Get a list of Pets"""
#     #     self._create_pets(5)
#     #     resp = self.app.get(BASE_URL)
#     #     self.assertEqual(resp.status_code, status.HTTP_200_OK)
#     #     data = resp.get_json()
#     #     self.assertEqual(len(data), 5)

#     def test_get_pet(self):
#         """Get a single Wishlist"""
#         # get the id of a pet
#         wishlist= Wishlist(name="test",customer=123456)
#         test_pet = Wishlist(name="test",customer=123456)
#         resp = self.app.get(
#             "/wishlist/{}".format(wishlist.customer), content_type=CONTENT_TYPE_JSON
#         )
#         self.assertEqual(resp.status_code, status.HTTP_200_OK)
#         data = resp.get_json()
#         self.assertEqual(data["name"], test_pet.name)

# def test_get_pet_not_found(self):
#     """Get a Pet thats not found"""
#     resp = self.app.get("/pets/0")
#     self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_wishlist(self):
      """Create a new Wishlist"""
      test_wishlist = WishlistFactory()
      logging.debug(test_wishlist)
      resp = self.app.post(
          BASE_URL, json=test_wishlist.serialize(), content_type=CONTENT_TYPE_JSON
      )
      self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
      # # Make sure location header is set
      # location = resp.headers.get("Location", None)
      # self.assertIsNotNone(location)
      # # Check the data is correct
      # new_wishlist = resp.get_json()
      # self.assertEqual(new_wishlist["name"], new_wishlist.name, "Names do not match")
      # self.assertEqual(
      #     new_wishlist["customer_id"], new_wishlist.customer_id, "customer_id do not match"
      # )
      # self.assertEqual(
      #     new_wishlist["products"], new_wishlist.products, "products does not match"
      # )
      # # Check that the location header was correct
      # resp = self.app.get(location, content_type=CONTENT_TYPE_JSON)
      # self.assertEqual(resp.status_code, status.HTTP_200_OK)
      # new_wishlist = resp.get_json()
      # nosetestsself.assertEqual(new_wishlist["name"], new_wishlist.name, "Names do not match")
      # self.assertEqual(
      #     new_wishlist["customer_id"], new_wishlist.customer_id, "customer_id do not match"
      # )
      # self.assertEqual(
      #     new_wishlist["products"], new_wishlist.products, "products does not match"
      # )

    def test_create_pet_no_data(self):
        """Create a wishlist with missing data"""
        resp = self.app.post(BASE_URL, json={}, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

# def test_create_pet_no_content_type(self):
#     """Create a Pet with no content type"""
#     resp = self.app.post(BASE_URL)
#     self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

# def test_create_pet_bad_available(self):
#     """ Create a Pet with bad available data """
#     test_pet = PetFactory()
#     logging.debug(test_pet)
#     # change available to a string
#     test_pet.available = "true"
#     resp = self.app.post(
#         BASE_URL, json=test_pet.serialize(), content_type="application/json"
#     )
#     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

# def test_create_pet_bad_gender(self):
#     """ Create a Pet with bad available data """
#     pet = PetFactory()
#     logging.debug(pet)
#     # change gender to a bad string
#     test_pet = pet.serialize()
#     test_pet["gender"] = "male"    # wrong case
#     resp = self.app.post(
#         BASE_URL, json=test_pet, content_type="application/json"
#     )
#     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

# def test_update_pet(self):
#     """Update an existing Pet"""
#     # create a pet to update
#     test_pet = PetFactory()
#     resp = self.app.post(
#         BASE_URL, json=test_pet.serialize(), content_type=CONTENT_TYPE_JSON
#     )
#     self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

#     # update the pet
#     new_pet = resp.get_json()
#     logging.debug(new_pet)
#     new_pet["category"] = "unknown"
#     resp = self.app.put(
#         "/pets/{}".format(new_pet["id"]),
#         json=new_pet,
#         content_type=CONTENT_TYPE_JSON,
#     )
#     self.assertEqual(resp.status_code, status.HTTP_200_OK)
#     updated_pet = resp.get_json()
#     self.assertEqual(updated_pet["category"], "unknown")

# def test_delete_pet(self):
#     """Delete a Pet"""
#     test_pet = self._create_pets(1)[0]
#     resp = self.app.delete(
#         "{0}/{1}".format(BASE_URL, test_pet.id), content_type=CONTENT_TYPE_JSON
#     )
#     self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
#     self.assertEqual(len(resp.data), 0)
#     # make sure they are deleted
#     resp = self.app.get(
#         "{0}/{1}".format(BASE_URL, test_pet.id), content_type=CONTENT_TYPE_JSON
#     )
#     self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

# def test_query_pet_list_by_category(self):
#     """Query Pets by Category"""
#     pets = self._create_pets(10)
#     test_category = pets[0].category
#     category_pets = [pet for pet in pets if pet.category == test_category]
#     resp = self.app.get(
#         BASE_URL, query_string="category={}".format(quote_plus(test_category))
#     )
#     self.assertEqual(resp.status_code, status.HTTP_200_OK)
#     data = resp.get_json()
#     self.assertEqual(len(data), len(category_pets))
#     # check the data just to be sure
#     for pet in data:
#         self.assertEqual(pet["category"], test_category)

# @patch('service.routes.Pet.find_by_name')
# def test_bad_request(self, bad_request_mock):
#     """ Test a Bad Request error from Find By Name """
#     bad_request_mock.side_effect = DataValidationError()
#     resp = self.app.get(BASE_URL, query_string='name=fido')
#     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

# @patch('service.routes.Pet.find_by_name')
# def test_mock_search_data(self, pet_find_mock):
#     """ Test showing how to mock data """
#     pet_find_mock.return_value = [MagicMock(serialize=lambda: {'name': 'fido'})]
#     resp = self.app.get(BASE_URL, query_string='name=fido')
#     self.assertEqual(resp.status_code, status.HTTP_200_OK)

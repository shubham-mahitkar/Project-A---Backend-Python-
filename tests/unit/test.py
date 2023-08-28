import unittest
import os
import sys
from flask.testing import FlaskClient
from unittest.mock import patch
import json
from flask.wrappers import Response

# Add app path to module path
# sys.path.append(os.path.dirname(os.path.realpath(__file__).rsplit('/', 2)[0]))
# from app import app
# from app.users.models import Users

# from users.app import app
# app1 = app

import requests
class TestUsers(unittest.TestCase):

    def test_get_hello(self):
        response = requests.get('http://localhost:5000/users')
        assert response.status_code == 200
        print("Read Successful", response)
    #     response_body = response.text
    #     print("response_body: ", response_body)


    # def test_01_add(self):
    #     info = {"name": "value1", "email": "value2"}
    #     rv = requests.post('http://localhost:5000/add', json.dumps(info), headers={'Content-Type': 'application/json'})
    #     assert 'Add was successful'
    #     print("Add was successful ", rv)


    def test_02_update(self):
        info = {"id": 43, "name": "test string", "email": "testing@flask.pocoo.com", "password":"test string"}        
        rv = requests.put('http://localhost:5000/update', json.dumps(info), headers={'Content-Type': 'application/json'})
        assert 'Update was successful'
        print("update: ", rv)


    # def test_03_delete(self):
    #     id = 3
    #     info = {"name": "test string", "email": "testing@flask.pocoo.com", "password":"test string"}        
    #     rv = requests.delete('http://localhost:5000/delete/{}'.format(id))
    #     assert 'Delete was successful'
    #     print("deleted was successful ", rv)





# import pytest

# class TestUsers(unittest.TestCase):
#     @pytest.fixture
#     def client():
#         with app.test_client() as client:
#             yield client

#     class TestSomething:
#         def test_this(self, client):
#             res = client.get('/users', follow_redirects=True)
#             print("res: : - ", res)
#             assert res.status_code == 200







if __name__ == '__main__':
    unittest.main()
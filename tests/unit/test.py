import unittest
from flask.testing import FlaskClient
from unittest.mock import patch
import json
from flask.wrappers import Response
import requests


class TestUsers(unittest.TestCase):

    def test_00_read(self):
        response = requests.get('http://localhost:5000/users')
        assert response.status_code == 200
        print("Read Successful", response)
    #     response_body = response.text
    #     print("response_body: ", response_body)


    def test_01_add(self):
        info = {"name": "value1", "email": "value2@gmail.com"}
        rv = requests.post('http://localhost:5000/add', json.dumps(info), headers={'Content-Type': 'application/json'})
        assert 'Add was successful'
        print("Add was successful ", rv)


    def test_02_update(self):
        info = {"id": 123, "name": "test string", "email": "testing@flask.pocoo.com", "password":"test string"}        
        rv = requests.put('http://localhost:5000/update', json.dumps(info), headers={'Content-Type': 'application/json'})
        assert 'Update was successful'
        print("update: ", rv)


    def test_03_delete(self):
        id = 125      
        rv = requests.delete('http://localhost:5000/delete/{}'.format(id))
        assert 'Delete was successful'
        print("deleted was successful ", rv)


if __name__ == '__main__':
    unittest.main()

#python -m unittest tests\unit\test.py
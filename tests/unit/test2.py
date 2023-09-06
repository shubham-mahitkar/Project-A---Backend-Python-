import unittest
from unittest.mock import patch
from users.app import app


from tests.unit.confest import client


def test_should_status_code_ok(client):
	response = client.get('/users')
	assert response.status_code == 200












# class TestAPI(unittest.TestCase):
#     def setUp(self):
#         self.app = app.test_client()

#     def tearDown(self):
#         pass


#     @patch('users.handlers.user')
#     def test_get_user_info_endpoint(self, mock_get_user_info):
#         mock_get_user_info.return_value = {'id': 1, 'name': 'shubham', 'email': 'shubham@gmail.com'}

#         response = self.app.get('/users/')

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json, {'id': 1, 'name': 'shubham'})

#     @patch('my_app.api.views.get_user_info')
#     def test_get_user_info_not_found(self, mock_get_user_info):
#         mock_get_user_info.return_value = None

#         response = self.app.get('/users/2')

#         self.assertEqual(response.status_code, 404)



if __name__ == '__main__':
    unittest.main()
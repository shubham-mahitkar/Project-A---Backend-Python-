import json
from unittest.mock import patch

# ########Read#########
@patch("users.handlers.UserModel")
@patch("users.handlers.CypherModel")
def test_get_users(mock_cypher_model, mock_user_model, client):
    """Test GET /users endpoint."""

    mock_user_model().get_users.return_value = [
        {'id': 100, 'name': 'namrata', 'email': 'npatel@test.com', 'password': 'foo'}
    ]
    mock_cypher_model().get_users.return_value = [{'name': 'Namrata', 'application': 'Facebook', 'neo_id': 294}]

    response = client.get('/users')
    assert response.status_code == 200

    actual_result = json.loads(response.data)
    expected_result = [
        {'email': 'npatel@test.com', 'id': 100, 'name': 'namrata', 'password': 'foo'}
    ]
    assert actual_result == expected_result


# #######Delete#########
# @patch("users.handlers.UserModel")
# def test_delete_user(mock_model, client):
#     """Test DELETE /delete endpoint."""
#     mock_model().delete_user.return_value = [
#         "User deleted successfully!"
#     ]

#     response = client.delete('/delete/100')
#     assert response.status_code == 200
#     actual_result = json.loads(response.data)
#     assert actual_result == {"result":'User deleted successfully!'}


# ########Create#########
# @patch("users.handlers.UserModel")
# def test_add_user(mock_model, client):
#     """Test POST /add endpoint."""
#     expected_response = {'id': 234, 'name': 'shubham', 'email': 'shubham@test.com', 'password': 'foo', "application": [
#             "Facebook"
#         ]}
#     mock_model().add_user.return_value = expected_response
#     response = client.post('/add', json=expected_response)
#     print("response.json : ", response.json)
#     assert response.status_code == 200
#     actual_result = response.json
#     assert actual_result == expected_response


########Update#########
# @patch("users.handlers.UserModel")
# def test_update_user(mock_model, client):
#     """Test PUT /update endpoint."""
#     id = 101
#     expected_response = {'name': 'shubham', 'email': 'shubham@test.com', 'id':id, 'application': ['Facebook']}
    
#     mock_model().update_user.return_value = expected_response
#     formdatadict = {'name': 'shubham', 'email': 'shubham@test.com', 'id': 101, 'application': ['Facebook']}
#     response = client.put('/update/101', data=json.dumps(formdatadict), content_type='application/json')
#     assert response.status_code == 200
#     actual_result = json.loads(response.data)
#     assert actual_result == expected_response


# @patch("users.handlers.UserModel")
# def test_get_user(mock_model, client):
#     """Test GET /user/ endpoint."""
#     id = 101
#     expected_response = [
#     {
#         "application": [
#             "Youtube"
#         ],
#         "email": "ramupdate2@gmail.com",
#         "id": id,
#         "name": "ram",
#         "password": "pbkdf2:sha256:600000$7blUGE7X47wfLhA5$812e9717924855df00688f81d5c8b84b7a1878af7637d523a286c7a1732c7fff"
#     }
# ]
#     a = mock_model().user.return_value = expected_response
#     print("a: ", a)

#     response = client.get(f"/user/{id}")
#     assert response.status_code == 200
#     actual_result = json.loads(response.data)
#     assert actual_result == expected_response

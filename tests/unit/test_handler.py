import json
from unittest.mock import patch


# ########Read#########
@patch("users.handlers.UserModel")
@patch("users.handlers.CypherModel")
def test_get_users(mock_cypher_model, mock_user_model, client):
    """Test GET /users endpoint."""

    mock_user_model().get_users.return_value = [
        {'id': 100, 'name': 'namrata', 'email': 'npatel@test.com', 'password': 'foo'},
        {'id': 101, 'name': 'shubham', 'email': 'shubham@test.com', 'password': 'foo'},
    ]
    mock_cypher_model().get_users_applications_from_neo4j.return_value = [
        {'name': 'namrata', 'application': 'Facebook', 'neo_id': 100}
    ]

    response = client.get('/users')
    assert response.status_code == 200

    actual_result = json.loads(response.data)
    expected_result = [
        {
            'email': 'npatel@test.com',
            'id': 100,
            'name': 'namrata',
            'password': 'foo',
            'application': ['Facebook']
        }, {
            'email': 'shubham@test.com',
            'id': 101,
            'name': 'shubham',
            'password': 'foo',
        }
    ]
    assert actual_result == expected_result


# #######Delete#########
@patch("users.handlers.UserModel")
@patch("users.handlers.CypherModel")
def test_delete_user(mock_model, mock_cypher_model, client):
    """Test DELETE /delete endpoint."""

    mock_model().delete_user.return_value = [
        "User deleted successfully!"
    ]
    mock_cypher_model().delete_user_application.return_value = [
        "User deleted successfully!"
    ]

    response = client.delete('/delete/100')
    assert response.status_code == 200

    actual_result = json.loads(response.data)
    assert actual_result == {"result":'User deleted successfully!'}


# ########Create#########
@patch("users.handlers.UserModel")
@patch("users.handlers.CypherModel")
def test_add_user(mock_neo4j, mock_model, client):
    """Test POST /add endpoint."""
    expected_response = {'id': 234, 'name': 'shubham', 'email': 'shubham@test.com', 'password': 'foo', 'application': ['Facebook']}
    expected_response_neo4j = {'application': ['Facebook']}

    user_model_instance = mock_model.return_value
    user_model_instance.add_user.return_value = expected_response

    cypher_model_instance = mock_neo4j.return_value
    cypher_model_instance.add_user_application.return_value = expected_response_neo4j

    response = client.post('/add', json=expected_response)
    assert response.status_code == 200

    actual_result = response.json
    assert actual_result == expected_response


########Update#########
@patch("users.handlers.UserModel")
@patch("users.handlers.CypherModel")
def test_update_user(mock_neo4j, mock_model, client):
    """Test PUT /update endpoint."""
    id = 101
    expected_response = {'name': 'shubham', 'email': 'shubham@test.com', 'id': id}
    expected_response_neo4j = {'application': ['Facebook']}

    user_model_instance = mock_model.return_value
    user_model_instance.update_user.return_value = expected_response

    cypher_model_instance = mock_neo4j.return_value
    cypher_model_instance.update_user_applications_by_id.return_value = expected_response_neo4j

    formdatadict = {'name': 'shubham', 'email': 'shubham@test.com', 'id': id, 'application': ['Facebook']}
    response = client.put(f'/update/{id}', data=json.dumps(formdatadict), content_type='application/json')
    assert response.status_code == 200

    actual_result = json.loads(response.data)
    assert actual_result == expected_response

import json
from unittest.mock import patch


@patch("users.handlers.UserModel")
def test_get_users(mock_model, client):
    """Test GET /users endpoint."""
    mock_model().get_users.return_value = [
        {'id': 100, 'name': 'namrata', 'email': 'npatel@test.com', 'password': 'foo'}
    ]

    response = client.get('/users')
    print(response.data)
    assert response.status_code == 200
    actual_result = json.loads(response.data)
    assert actual_result == [{
        'email': 'npatel@test.com', 'id': 100, 'name': 'namrata',
        'password': 'foo'
    }]

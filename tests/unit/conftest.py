from unittest import mock
from unittest.mock import patch, Mock, MagicMock

import pytest
import neo4j
import snowflake.connector


@pytest.fixture
def mock_neo4j(mocker):
    mock_conn = Mock(spec=neo4j.GraphDatabase)
    mocker.patch('neo4j.GraphDatabase', return_value=mock_conn)
    return mock_conn


@pytest.fixture
def mock_snowflake(mocker):
    mock_cursor = MagicMock()
    mocker.patch('snowflake.connector.connect', return_value=mock_cursor)
    return mock_cursor


@pytest.fixture
def client(mock_neo4j, mock_snowflake):
    from users.app import app
    with app.test_client() as client:
        yield client

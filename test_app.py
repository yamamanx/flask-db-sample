import pytest
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('app.get_db_connection')
def test_index(mock_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [(1, 'Test Title', 'Test Content')]
    mock_conn.cursor.return_value = mock_cursor
    mock_db.return_value = mock_conn
    
    response = client.get('/')
    assert response.status_code == 200

@patch('app.get_db_connection')
def test_create_get(mock_db, client):
    response = client.get('/create')
    assert response.status_code == 200

@patch('app.get_db_connection')
def test_create_post(mock_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_db.return_value = mock_conn
    
    response = client.post('/create', data={'title': 'Test', 'content': 'Test Content'})
    assert response.status_code == 302
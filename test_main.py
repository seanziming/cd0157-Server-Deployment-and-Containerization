'''
Tests for jwt flask app.
'''
import os
import json
import datetime
import jwt

# Set the JWT_SECRET BEFORE importing main
os.environ['JWT_SECRET'] = 'TestSecret'

import pytest
import main

SECRET = 'TestSecret'
EMAIL = 'wolf@thedoor.com'
PASSWORD = 'huff-puff'

@pytest.fixture
def client():
    # Ensure the secret is still set (in case of module caching)
    os.environ['JWT_SECRET'] = SECRET
    main.JWT_SECRET = SECRET  # Also set it directly on the module
    main.APP.config['TESTING'] = True
    client = main.APP.test_client()

    yield client



def test_health(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == 'Healthy'


def test_auth(client):
    body = {'email': EMAIL,
            'password': PASSWORD}
    response = client.post('/auth', 
                           data=json.dumps(body),
                           content_type='application/json')

    assert response.status_code == 200
    token = response.json['token']
    assert token is not None


def test_contents(client):
    """
    Test the /contents endpoint with a valid JWT token
    """
    # Create a valid token for testing
    exp_time = datetime.datetime.utcnow() + datetime.timedelta(weeks=2)
    payload = {
        'exp': exp_time,
        'nbf': datetime.datetime.utcnow(),
        'email': EMAIL
    }
    token = jwt.encode(payload, SECRET, algorithm='HS256')
    
    # PyJWT 1.7.1 returns bytes, decode to string
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    
    response = client.get('/contents',
                         headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 200
    assert 'email' in response.json
    assert response.json['email'] == EMAIL


def test_contents_without_token(client):
    """
    Test the /contents endpoint without a token (should fail)
    """
    response = client.get('/contents')
    assert response.status_code == 401


def test_contents_with_invalid_token(client):
    """
    Test the /contents endpoint with an invalid token (should fail)
    """
    response = client.get('/contents',
                         headers={'Authorization': 'Bearer invalid-token'})
    assert response.status_code == 401

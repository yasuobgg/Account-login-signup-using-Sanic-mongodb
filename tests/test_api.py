# Import the Sanic app, usually created with Sanic(__name__)
# import pytest
from api import app
import json
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJoZWxsb3dvcmxkIjoiaGVsbG93b3JsZCJ9.DlFqxmM6GscfH_b4K0ARD11yEziWL_WjpFQFjn0fv2A"

def test_index_returns_200():
    request, response = app.test_client.post('/jwt')
    assert response.status == 200
    assert "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" in response.text

def test_index_put_not_allowed():
    request, response = app.test_client.get('/jwt')
    assert response.status == 405

def test_valid_login():
    data = {"username": "user1", "password": "pass1"}
    request, response = app.test_client.post('/login', headers={'Authorization': f'Bearer {token}'}, data=json.dumps(data))
    assert response.status == 200
    assert response.text == "welcome"

def test_invalid_jwt():
    data = {"username": "user1", "password": "pass1"}
    request, response = app.test_client.post('/login', headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJoZWxsb3dvcmxkIjoiaGVsbG93b3JsZCJ9.BAD'}, data=json.dumps(data))
    assert response.status == 401
    assert response.text == "You are unauthorized."

def test_invalid_username():
    data = {"username": "user0", "password": "pass1"}
    request, response = app.test_client.post('/login', headers={'Authorization': f'Bearer {token}'}, data=json.dumps(data))
    assert response.status == 200
    assert response.text == "incorrect username"

def test_invalid_password():
    data = {"username": "user1", "password": "pass2"}
    request, response = app.test_client.post('/login', headers={'Authorization': f'Bearer {token}'}, data=json.dumps(data))
    assert response.status == 200
    assert response.text == "incorrect password"

"__________________________________________________________________________________"

# def test_valid_signup():
#     data = {"username": "usersdasd", "password": "pass"}
#     request, response = app.test_client.post('/signup', headers={'Authorization': f'Bearer {token}'}, data=json.dumps(data))
#     # assert response.status == 201
#     assert response.text == '"created"'

def test_exis_username_signup():
    data = {"username": "user1", "password": "pass1"}
    request, response = app.test_client.post('/signup', headers={'Authorization': f'Bearer {token}'}, data=json.dumps(data))
    assert response.status == 200
    assert "username already exis" in response.text
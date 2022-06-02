from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_related():
    response = client.get('/related/go')
    assert response.json()['words'][0]=='going'

def test_create_user():
    response = client.post(
        '/users/',
        json={"username":'ezio','password':'go'},
    )
    assert response.json()['username'] =='ezio'

def test_delete_user():
    response = client.delete(
        '/users/',
        json={"username":'ezio'},
    )
    assert response.json()['username'] =='ezio'

# def test_create_user():
#     response = client.post(
#         '/user/',
#         json={"username":'hgfds','password':'go','email':'hello@ox.ac.uk'}
#     )
#     assert response.status_code == 200
#     assert response.json()['data'][0]['email'] == 'hello@ox.ac.uk'

# def test_getuser():
#     response = client.get('/user/6298fd14d72582a0449af964')
#     assert response.json()['data'][0]['username']=='foo'

# def test_delete_user():
#     response = client.delete(
#         '/user/6298fd14d72582a0449af964',
#         json={"username":'hgfds','password':'go','email':'hello@ox.ac.uk'}
#     )
#     assert response.status_code == 200
#     assert response.json()['data'][0]['email'] == 'hello@ox.ac.uk'


def test_():
    response = client.get("/")
    assert response.status_code == 401
    # assert response.json() == {"msg": "Hello World"}

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_related():
    response = client.get('/related/go')
    assert response.json()['words'][0]=='going'

def test_create_user():
    response = client.post(
        '/users/',
        json={"username":'ez','password':'go'},
    )
    assert response.json()['username'] =='ez'

def test_delete_user():
    response = client.delete(
        '/users/',
        json={"username":'ez'},
    )
    assert response.json()['username'] =='ez'

def test_get_journal():
    response = client.get('/users/journals/')
    assert response.json()[0]['title'] =='string'

def test_add_new_journal_for_user():
    response = client.post(
        "/users/12/journals/",
        json={"title":"test","date":"test","body":"test"},
        )
    assert response.json()['title'] =='test'

def test_delete_journal():
    response = client.delete(
        "/users/12/journals/",
        json={"title":"test"},
        )
    print(response.json())
    assert response.json()['title'] =='test'
    

def test_():
    response = client.get("/")
    assert response.status_code == 401
    # assert response.json() == {"msg": "Hello World"}

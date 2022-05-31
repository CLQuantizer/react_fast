from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_related():
    response = client.get('/related/go')
    print(response)
    assert response.json()['words'][0]=='going'

def test_journal():
    response = client.get('/journal/629642d565b313aa5eb625d3')
    print(response)
    assert response.json()['data'][0]['author'] =='Ezius'

def test_():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


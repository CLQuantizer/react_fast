from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_related():
    response = client.post('/related/go')
    print(response)
    assert response.json()['words'][0]=='going'

def test_():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


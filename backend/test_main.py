from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

MAGIC_WORD = "go"
MAGIC_NAME = "ez"

def test_related():
    response = client.get('/related/'+MAGIC_WORD)
    assert response.json()['words'][0]=='going'

def test_create_user():
    response = client.post(
        '/users/',
        json={"username": MAGIC_NAME,'password':MAGIC_WORD},
    )
    assert response.json()['username']== MAGIC_NAME

def test_get_user_by_username():
    response = client.get("/users/username/"+MAGIC_NAME)
    assert response.json()['username']== MAGIC_NAME

def test_get_user_by_id():
    response1 = client.get("/users/user_id/59/")
    assert response1.json()['username'] == "Joe"

def test_delete_user():
    response = client.delete(
        '/users/username/'+MAGIC_NAME,
    )
    assert response.json()['username']==MAGIC_NAME

def test_jwt_login():
    response = client.post(
        headers={"Content-Type":"application/x-www-form-urlencoded"},
        url ="/users/token",
        data = "grant_type=&username=Joe&password=Joe&scope=&client_id=&client_secret="
    )
    assert response.json()['token_type']== 'bearer'
    assert response.status_code == 200

def test_add_new_journal_for_user():
    response = client.post(
        "/users/user_id/59/journals/",
        json={"title":"test","date":"test","body":"test"},
        )
    assert response.json()['title'] =='test'

# get journal must be between add new and delete
def test_get_journal():
    response = client.get('/users/journals/')
    assert response.json()[0]['title']=='test'

def test_delete_journal():
    response = client.delete(
        "/users/user_id/59/journals/",
        json={"title":"test"},
        )
    assert response.json()['title']=='test'
    

def test_():
    response = client.get("/")
    assert response.status_code == 401
    # assert response.json() == {"msg": "Hello World"}

import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    res = client.get('/')
    assert res.status_code == 200

    json_data = res.get_json()
    assert json_data is not None
    assert json_data.get('message') == "Backend Flask funcionando correctamente"




import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b"API Funcionando" in res.data

import pytest
from app import app

@pytest.fixture
def client():
    return app.test_client()

def test_home(client):
    res = client.get('/')
    assert res.status_code == 200

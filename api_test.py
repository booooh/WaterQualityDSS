import pytest
import api as service

@pytest.fixture
def api():
    return service.api


def test_hello_world(api):
    r = api.requests.get("/")
    assert r.text == "hello, world!"

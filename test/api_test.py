import time

import pytest

import api as service
import processing

@pytest.fixture
def api():
    return service.api

def test_execution_not_found(api):
    assert api.requests.get(f"/status/DOES_NOT_EXIST").json()['status'] == 'NOT_FOUND'

def test_model_execution(api, tmp_path):
    file_obj = tmp_path / "data.t"
    file_obj.write_bytes("this is some value".encode())
    PROCESSING_DURATION = 3
    
    files = {'model': (file_obj.name, file_obj.read_bytes(), 'application/octet-stream')}
    data = {'processing_duration' : PROCESSING_DURATION}
    resp = api.requests.post("/model", files=files, data=data)    
    model_response = resp.json()
    assert 'id' in model_response
    exec_id = model_response['id']

    assert api.requests.get(f"/status/{exec_id}").json()['status'] == 'RUNNING'
    time.sleep(PROCESSING_DURATION + 2)
    assert api.requests.get(f"/status/{exec_id}").json()['status'] == 'COMPLETED'



import time

import pytest

import api as service
import processing

@pytest.fixture
def api():
    return service.api

def test_execution_not_found(api):
    assert api.requests.get(f"/status/DOES_NOT_EXIST").json()['status'] == 'NOT_FOUND'

def test_dss_execution(api, tmp_path):
    CONTENTS="this is some value"

    file_obj = tmp_path / "data.t"
    file_obj.write_bytes(CONTENTS.encode())
    PROCESSING_DURATION = 1
    
    files = {'model': (file_obj.name, file_obj.read_bytes(), 'application/octet-stream')}
    data = {'processing_duration' : PROCESSING_DURATION}
    resp = api.requests.post("/dss", data=data, files=files)    
    model_response = resp.json()
    assert 'id' in model_response
    exec_id = model_response['id']

    assert api.requests.get(f"/status/{exec_id}").json()['status'] == processing.ExectuionState.RUNNING.value
    time.sleep(PROCESSING_DURATION + 0.1)
    resp = api.requests.get(f"/status/{exec_id}").json()    
    assert resp['status'] == processing.ExectuionState.COMPLETED.value
    assert resp['result'] == CONTENTS



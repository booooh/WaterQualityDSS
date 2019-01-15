import threading
import unittest.mock as mock
import pytest

import api as service
import processing

@pytest.fixture
def api():
    return service.api

def test_execution_not_found(api):
    assert api.requests.get(f"/status/DOES_NOT_EXIST").json()['status'] == 'NOT_FOUND'

def test_dss_execution(api, tmp_path):
    '''
    Test the execution of a dss, including setting the paramters, and polling for a result
    '''
    CONTENTS="this is some value"
   
    file_obj = tmp_path / "data.t"
    file_obj.write_bytes(CONTENTS.encode())
    PROCESSING_DURATION = 1
    
    files = {'model': (file_obj.name, file_obj.read_bytes(), 'application/octet-stream')}
    data = {'processing_duration' : PROCESSING_DURATION}
    
    completion_event = threading.Event()
    start_event = threading.Event()

    def complete(*args, **kwargs):
        start_event.wait()
        completion_event.set()

    with mock.patch('processing.exec_model') as exec_model:     
        with mock.patch('processing.prepare_run_dir'):
            exec_model.side_effect = complete
            resp = api.requests.post("/dss", data=data, files=files)        

    model_response = resp.json()
    assert 'id' in model_response
    exec_id = model_response['id']

    # we check for the running state before allowing the model to complete
    assert api.requests.get(f"/status/{exec_id}").json()['status'] == processing.ExectuionState.RUNNING.value

    # the model can now complete
    start_event.set()

    # wait for execution to complete
    completion_event.wait()        
    resp = api.requests.get(f"/status/{exec_id}").json()                
    assert resp['status'] == processing.ExectuionState.COMPLETED.value
    assert resp['result'] == CONTENTS



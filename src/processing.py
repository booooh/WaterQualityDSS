from enum import Enum
import os
import shutil
from subprocess import check_call
import tempfile
import uuid

EXECUTIONS = {}

MODEL_EXE=os.environ.get("WQDSS_MODEL_EXE", "linux_model_v3_71")
BASE_MODEL_DIR= os.environ.get("WQDSS_BASE_MODEL_DIR", "/model")

class ExectuionState(Enum):    
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'

class Execution:
    def __init__(self, state=ExectuionState.RUNNING):
        self.state = state
        self.result = None
        self.runs = []

    def add_run(self, run_dir):
        self.runs.append(run_dir)

    def clean(self):
        for run_dir in self.runs:
            shutil.rmtree(run_dir)

def prepare_run_dir(exec_id, params):
    '''
    Populates a temporary directory with the model files, 
    along with inputs provided by the user
    '''
    
    run_dir = tempfile.mkdtemp(prefix=f'wqdss-exec-{exec_id}')
    shutil.copytree(BASE_MODEL_DIR, os.path.join(run_dir, "model"))
    
    #TODO: extract content from params that may be used to update the model 
    return run_dir


def exec_model(model_dir, params):    
    check_call([MODEL_EXE, model_dir])

def get_exec_id():
    return str(uuid.uuid4())

def get_status(exec_id):
    return EXECUTIONS[exec_id].state.value

def get_result(exec_id):
    return EXECUTIONS[exec_id].result

def execute_dss(exec_id, params):
    #TODO: extract handling the Execution to a context
    current_execution =  Execution()
    EXECUTIONS[exec_id] = current_execution    
    
    #TODO: implement logic for DSS. For now - just a single run, and mock results
    run_dir = prepare_run_dir(exec_id, params)
    current_execution.add_run(run_dir)
    exec_model(run_dir, params)
    current_execution.result = params['model']['content']
    current_execution.state = ExectuionState.COMPLETED
    
    


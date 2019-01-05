from enum import Enum
import time
import uuid

EXECUTIONS = {}
class ExectuionState(Enum):
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'

class ExecutionResult:
    def __init__(self, state=ExectuionState.RUNNING):
        self.state = state
        self.result = None

def get_exec_id():
    return str(uuid.uuid4())

def get_status(exec_id):
    return EXECUTIONS[exec_id].state.value

def get_result(exec_id):
    return EXECUTIONS[exec_id].result

def execute_dss(exec_id, params):
    EXECUTIONS[exec_id] = ExecutionResult()
    time.sleep(float(params['processing_duration']))    
    EXECUTIONS[exec_id].state = ExectuionState.COMPLETED
    EXECUTIONS[exec_id].result = params['model']['content']
    


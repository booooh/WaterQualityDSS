import time
import uuid

EXECUTIONS = {}

def get_exec_id():
    return str(uuid.uuid4())

def execute_model(exec_id, params):
    EXECUTIONS[exec_id] = 'RUNNING'
    print(f'{exec_id}: going to run the model with {params}')
    time.sleep(3)
    EXECUTIONS[exec_id] = 'COMPLETED'
    


from enum import Enum
import os
import random
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
    def __init__(self, exec_id, state=ExectuionState.RUNNING):
        self.state = state
        self.result = None
        self.exec_id = exec_id
        self.runs = []
        EXECUTIONS[exec_id] = self

    def add_run(self, run_dir):
        self.runs.append(run_dir)

    def clean(self):
        for run_dir in self.runs:
            shutil.rmtree(run_dir)

    def mark_complete(self):
        self.state = ExectuionState.COMPLETED

    def execute(self, params):
        run_dir = prepare_run_dir(self.exec_id, params)
        #TODO: implement logic for DSS. For now - just a single run, and mock results    
        self.add_run(run_dir)
        exec_model(run_dir, params)
        return {'best_run': 0, 'score': get_run_score(run_dir, params)}
        


def prepare_run_dir(exec_id, params):
    '''
    Populates a temporary directory with the model files, 
    along with inputs provided by the user
    '''
    
    run_dir = tempfile.mkdtemp(prefix=f'wqdss-exec-{exec_id}')
    shutil.copytree(BASE_MODEL_DIR, os.path.join(run_dir, "model"))
    
    #TODO: extract content from params that may be used to update the model 
    return run_dir


def exec_model(run_dir, params):    
    check_call([MODEL_EXE, run_dir])

def get_run_parameter_value(run_dir, param_name, outfile):
    """
    Parses outfile (csv file) and extracts the value for the field named as `param_name` from the last row
    """

    #TODO: implement, for now returning a random value
    return random.uniform(-5.0, 5.0)


def calc_param_score(value, target, score_step, desired_direction):
    
    if desired_direction > 0:
        distance = value - target
    else:
        distance = target - value

    return distance/score_step

def get_run_score(run_dir, params):
    """
    Based on the params field 'model_analysis' find the run for this score
    """
    model_analysis_params = params['model_analysis']['parameters']
    out_file = params['model_analysis']['output_file']

    param_scores = {}
    for param in model_analysis_params:
        param_value = get_run_parameter_value(run_dir, param['name'], out_file)
        param_score = calc_param_score(param_value, float(param['target']), float(param['score_step']), int(param['desired_direction']))
        param_scores[param['name']] = (param_score, float(param['weight']))

    weights = [s[1] for s in param_scores.values()]
    weighted_scores = [s[0] * s[1] for s in param_scores.values()]
    
    return sum(weighted_scores)/sum(weights)
        
def get_exec_id():
    return str(uuid.uuid4())

def get_status(exec_id):
    return EXECUTIONS[exec_id].state.value

def get_result(exec_id):
    return EXECUTIONS[exec_id].result


def execute_dss(exec_id, params):
    #TODO: extract handling the Execution to a context
    current_execution =  Execution(exec_id)
    try:
        result = current_execution.execute(params)
        current_execution.result = result
    finally:    
        current_execution.mark_complete()
    
    


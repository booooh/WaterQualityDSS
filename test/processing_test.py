from unittest.mock import patch
import processing

def test_execute_dss():    
    exec_id = 'foo'
    params = {
        'model_analysis' : {
            'parameters' : [
                {'name': 'NO3', 'target':'3.7', 'weight':'4', 'score_step':'0.1', 'desired_direction':'-1'},
                {'name': 'NH4', 'target':'2.4', 'weight':'2', 'score_step':'0.2', 'desired_direction':'-1'},
                {'name': 'DO', 'target':'8', 'weight':'2', 'score_step':'0.5', 'desired_direction':'+1'},
            ],
            'output_file': 'out.csv'
        },        
    }
    
    with patch('processing.exec_model') as exec_model:        
        with patch('processing.prepare_run_dir') as prepare_run_dir:
            processing.execute_dss(exec_id, params)            
        
    exec_model.assert_called_once()
    prepare_run_dir.assert_called_once()
        
from unittest.mock import patch
from pytest import approx

import processing

params = {
    'model_analysis' : {
        'parameters' : [
            {'name': 'NO3', 'target':'3.7', 'weight':'4', 'score_step':'0.1', 'desired_direction':'-1'},
            {'name': 'NH4', 'target':'2.4', 'weight':'2', 'score_step':'0.2', 'desired_direction':'-1'},
            {'name': 'DO', 'target':'8.0', 'weight':'2', 'score_step':'0.5', 'desired_direction':'+1'},
        ],
        'output_file': 'out.csv'
    },        
}

def test_execute_dss():    
    exec_id = 'foo'
    
    with patch('processing.exec_model') as exec_model:        
        with patch('processing.prepare_run_dir') as prepare_run_dir:
            processing.execute_dss(exec_id, params)            
        
    exec_model.assert_called_once()
    prepare_run_dir.assert_called_once()


def test_get_run_score():
    # test where all values are at their targets
    with patch('processing.get_run_parameter_value', side_effect=[3.7, 2.4, 8.0]):
        result = processing.get_run_score(None, params)
        assert result == 0

    # test where one value exceeds target (wrong direction)
    with patch('processing.get_run_parameter_value', side_effect=[3.7, 2.4, 7.0]):
        result = processing.get_run_score(None, params)
        assert result == approx(-0.5)  #  ((7.0 - 8.0)/0.5) * (2.0/8.0))

    # test where two values exceed target (wrong direction)
    with patch('processing.get_run_parameter_value', side_effect=[3.8, 2.4, 7.0]):
        result = processing.get_run_score(None, params)
        assert result == approx(-1.0)  #  ((3.7 - 3.8)/0.1)*(4.0/8.0)  + ((7.0 - 8.0)/0.5) * (2.0/(8.0))

    # test where two values exceed target (one in wrong direction, one in right direction)
    with patch('processing.get_run_parameter_value', side_effect=[3.6, 2.4, 7.0]):
        result = processing.get_run_score(None, params)
        assert result == approx(0)  #  ((3.7 - 3.6)/0.1)*(4.0/8.0)  + ((7.0 - 8.0)/0.5) * (2.0/(8.0))

    # test where two values exceed target (both in right direction)
    with patch('processing.get_run_parameter_value', side_effect=[3.6, 2.4, 9.0]):
        result = processing.get_run_score(None, params)
        assert result == approx(1.0)  #  ((3.7 - 3.6)/0.1)*(4.0/8.0)  + ((9.0 - 8.0)/0.5) * (2.0/(8.0))
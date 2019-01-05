# WaterQualityDSS
A DSS leveraging CE-QUAL-W2 

* Contains a back-end docker for running a REST interface for model execution
* Running locally (without docker): 
    * ```pipenv install -d --pre --skip-lock``` (note - this will ignore the locked versions - use with care)
    * ```PYTHONPATH=src/ pytest test/```    
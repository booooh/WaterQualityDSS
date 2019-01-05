import responder
import processing

api = responder.API()

@api.route("/status/{exec_id}")
async def status(req, resp, * , exec_id):
    if exec_id in processing.EXECUTIONS:
        resp.media = {"id" : exec_id, "status": processing.EXECUTIONS[exec_id]}
    else:
        resp.media = {"id" : exec_id, "status": "NOT_FOUND"}

@api.route("/model")
async def exec_model(req, resp):
    """
    Get the uploaded file, execute the model in the background
    """
    print("going to await data")
    params = await req.media("files")
    print(f"got {params.keys()}")    
    exec_id = processing.get_exec_id()
    
    @api.background.task
    def task():
        processing.execute_model(exec_id, params)
    
    task()
    resp.media = {"id" : exec_id}

if __name__ == "__main__":
    api.run()
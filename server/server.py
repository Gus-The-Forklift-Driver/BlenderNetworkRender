# https://fastapi.tiangolo.com/tutorial/path-params/
from http.client import ImproperConnectionState
import json
from fastapi import FastAPI, Header
import utils
import datetime

app = FastAPI()

task_manager = utils.TaskManager()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ping")
async def ping():
    return 'pong'


@app.get('/next_task')
def next_task(key: str | None = Header(default=None)):
    if utils.verify_key(key):
        pass
    next_task = task_manager.get_next_task()
    task_manager.save_current_status()
    return next_task


@app.post('/progress/{task_name}')
async def update_progress(task_name: str, status: str | float, key: str | None = Header(default=None)):
    # if utils.verify_key(key):
    #     pass
    if status == 'DONE':
        internal_status = task_manager.mark_task_done(task_name)
        task_manager.save_current_status()
        return internal_status
    elif status == 'FAILED':
        internal_status = task_manager.mark_task_failed(task_name)
        task_manager.save_current_status()
        return internal_status
    else:
        return 'wtf'


if __name__ == '__main__':
    import os
    uvicorn_location = 'C:/Users/benhu/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0/LocalCache/local-packages/Python310/Scripts/'
    os.system(uvicorn_location+'uvicorn server:app --reload')

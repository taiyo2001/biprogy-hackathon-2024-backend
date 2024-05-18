from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db_session import post_todo, get_todo, put_start_time
import datetime

app = FastAPI()

class Todo(BaseModel):
    worker: str
    task: str
    time: int
    id: str

class qa_archive(BaseModel):
    questioner: str
    respondent: str
    question: str
    answer: str
    evaluation: int
    comment: str


APPID=1

def get_time_now():
    time_now = datetime.datetime.now()
    time_data = time_now.strftime("%Y-%m-%d %H:%M")
    return time_data


@app.post("/todo/post")
async def todo_register(todo: Todo, status_code=201):
    # todo_data = todo.model_dump()

    todo_data = {
        "app": APPID,
        "record":{
            "worker":{
                "value": todo.worker
            },
            "task":{
                "value": todo.task
            },
            "time":{
                "value": todo.time
            }
        }
    }

    try:
        post_todo(todo_data)
        return {"message": "Todo registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to register Todo: {str(e)}")
    
@app.get("/todo/get")
async def todo_get():
    try:
        return get_todo()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get Todo: {str(e)}")
    
@app.put("/todo/put/start")
async def start_time_put(todo: Todo, status_code=201):
    time_now = get_time_now()
    start_data = {
        "app": APPID,
        "id": todo.id,
        "record":{
            "startTime": {
                "value": time_now
            }
        }
    }
    try:
        return put_start_time(start_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to put StartTime: {str(e)}")

# @app.post("/qa_archive/post")
# async def qa_archive_register(qa_archive: qa_archive, status_code=201):

#     qa_archive_data = qa_archive.model_dump()

#     try:
#         await (qa_archive_data)
#         return {"message": "QA Archive registered successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to register QA Archive: {str(e)}")

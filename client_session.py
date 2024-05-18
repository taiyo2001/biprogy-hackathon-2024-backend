from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db_session import post_todo, get_todo
import json

app = FastAPI()

class Todo(BaseModel):
    worker: str
    task: str
    time: int

class qa_archive(BaseModel):
    questioner: str
    respondent: str
    question: str
    answer: str
    evaluation: int
    comment: str

APPID=1


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

# @app.post("/qa_archive/post")
# async def qa_archive_register(qa_archive: qa_archive, status_code=201):

#     qa_archive_data = qa_archive.model_dump()

#     try:
#         await (qa_archive_data)
#         return {"message": "QA Archive registered successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to register QA Archive: {str(e)}")
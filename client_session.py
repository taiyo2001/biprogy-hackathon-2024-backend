from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel
from db_session import post_todo, get_todo, put_start_time
from datetime import datetime
from typing import Optional, List
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from db_session_qa import post_qa, get_qa

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

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def handler(request:Request, exc:RequestValidationError):
    print(exc)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class PostTodo(BaseModel):
    worker: str
    task: str
    time: int
    startTime: str
      
    @classmethod
    def from_dict(cls, obj: dict):
        return cls(
            worker=obj['worker']['value'],
            task=obj['task']['value'],
            time=int(obj['time']['value']),
            startTime=obj['startTime']['value'],
        )

class GetTodo(BaseModel):
    worker: str
    task: str
    time: int
    startTime: Optional[str]
    id: int

    @classmethod
    def from_dict(cls, obj: dict):
        return cls(
            worker=obj['worker']['value'],
            task=obj['task']['value'],
            time=int(obj['time']['value']),
            startTime=obj['startTime']['value'],
            id=obj['レコード番号']['value']
        )

class startTime(BaseModel):
    id: int

class endTodo(BaseModel):
    id: int

APPID=1
QA_APP_ID=4

def get_time_now():
    time_now = datetime.now()
    time_data = time_now.strftime("%Y-%m-%d %H:%M")
    print(time_data)
    return time_data

def calculate_trouble_level(start_time, task_time):
    start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
    current_time = datetime.now()
    diff_minutes = (current_time - start_time).total_seconds() / 60

    if diff_minutes <= task_time:
        trouble_level = 1 + 4 * (diff_minutes / task_time) 
    else:
        over_time_ratio = (diff_minutes - task_time) / task_time
        trouble_level = 6 + 4 * min(over_time_ratio, 1) 

    return round(trouble_level), round(diff_minutes - task_time)

@app.post("/todo/post")
async def todo_register(todo: PostTodo, status_code=201):
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
            },
            "startTime":{
                "value": "-1"
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
        response = get_todo()
        results = []

        if 'records' in response:
            for record in response['records']:
                todo = GetTodo.from_dict(record)

                if todo.startTime == "-1":
                    trouble_level = 0
                    over_time = 0
                else:
                    start_time = todo.startTime
                    task_time = todo.time

                    trouble_level, over_time = calculate_trouble_level(start_time, task_time)

                results.append({
                    "worker": todo.worker,
                    "task": todo.task,
                    "time": todo.time,
                    "trouble_level": trouble_level,
                    "id": todo.id,
                    "over_time": over_time
                })

            return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get Todo: {str(e)}")

@app.put("/todo/put/start")
async def start_time_put(id: int, status_code=201):
    time_now = get_time_now()
    start_data = {
        "app": APPID,
        "id": int(id),
        "record":{
            "startTime": {
                "value": time_now
            }
        }
    }
    try:
        put_start_time(start_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to put StartTime: {str(e)}")

@app.delete("/todo/put/end")
async def delete_todo(id: int, status_code=201):
    end_data = {
        "app": APPID,
        "ids": [id]
    }
    try:
        delete_todo(end_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to put StartTime: {str(e)}")

@app.get("/qa/get")
async def qa_get():
    try:
        return get_qa()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get Qa: {str(e)}")

@app.post("/qa/post")
async def qa_register(qa: qa_archive, status_code=201):
    # todo_data = todo.model_dump()

    qa_data = {
        "app": QA_APP_ID,
        "record":{
            "questioner":{
                "value": qa.questioner
            },
            "respondent":{
                "value": qa.respondent
            },
            "question":{
                "value": qa.question
            },
            "answer":{
                "value": qa.answer
            },
            "evaluation":{
                "value": qa.evaluation
            },
            "comment":{
                "value": qa.comment
            }
            
        }
    }

    try:
        post_qa(qa_data)
        return {"message": "Qa registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to register Qa: {str(e)}")
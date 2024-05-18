from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db_session import post_todo, get_todo, put_start_time
import datetime
import Optional

app = FastAPI()

class Todo(BaseModel):
    worker: str
    task: str
    time: int
    startTime: Optional[str]

class startTime(BaseModel):
    id: int

APPID=1

def get_time_now():
    time_now = datetime.datetime.now()
    time_data = time_now.strftime("%Y-%m-%dT%H:%M+09:00")
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
        todo: Todo = get_todo()
        if todo.startTime == "-1":
            trouble_level = 0
        else:
            start_time = datetime.strptime(todo.startTime, "%Y-%m-%d %H:%M")
            current_time = datetime.now()
            diff_minutes = (current_time - start_time).total_seconds() / 60
            task_time = todo.time

            if diff_minutes >= task_time * 2:
                trouble_level = 10
            elif diff_minutes <= task_time:
                trouble_level = 5 * diff_minutes / task_time
            else:
                trouble_level = 5 + 5 * (diff_minutes - task_time) / task_time

            trouble_level = round(trouble_level)

        return {
            "worker": todo.worker,
            "task": todo.task,
            "time": todo.time,
            "trouble_level": trouble_level
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get Todo: {str(e)}")
    
@app.put("/todo/put/start")
async def start_time_put(startTime: startTime, status_code=201):
    time_now = get_time_now()
    start_data = {
        "app": APPID,
        "id": startTime.id,
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
    

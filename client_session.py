from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db_session import db_post

app = FastAPI()

class Todo(BaseModel):
    worker: str
    task: str
    time: int



@app.post("/todo/post")
async def todo_register(todo: Todo, status_code=201):

    todo_data = todo.model_dump()

    try:
        await db_post(todo_data)
        return {"message": "Todo registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to register Todo: {str(e)}")

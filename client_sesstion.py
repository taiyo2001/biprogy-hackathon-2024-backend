from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Todo(BaseModel):
    worker: str
    task: str
    time: int



@app.post("/todo/post")

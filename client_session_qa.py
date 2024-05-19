from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db_session_qa import post_qa, get_qa
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

APPID=4

@app.post("/qa/post")
async def qa_register(qa: qa_archive, status_code=201):
    # todo_data = todo.model_dump()

    qa_data = {
        "app": APPID,
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


@app.get("/qa/get")
async def qa_get():
    print('!!!!!!!!!!!')
    try:
        return get_qa()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get Qa: {str(e)}")

# @app.post("/qa_archive/post")
# async def qa_archive_register(qa_archive: qa_archive, status_code=201):

#     qa_archive_data = qa_archive.model_dump()

#     try:
#         await (qa_archive_data)
#         return {"message": "QA Archive registered successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to register QA Archive: {str(e)}")
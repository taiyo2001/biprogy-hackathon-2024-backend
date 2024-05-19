from dotenv import load_dotenv
load_dotenv()

import os
import requests

from fastapi.encoders import jsonable_encoder

URL="https://cnkgbbz9x1h5.cybozu.com/k/v1/"
APPID=1
API_TOKEN=os.getenv("API_TOKEN")

# test for post
# PARAMS={
#   "app":APPID,
#   "record":{
#     "worker":{
#       "value":"鈴木"
#     },
#     "task":{
#         "value":"すやすや寝る"
#     },
#     "time":{
#         "value":"100"
#     }
#   }
# }

# test for put
PARAMS = {
    "app": APPID,
    "id": 3,
    "record": {
        "startTime": {
            "value": "2024-05-19 13:05"
        }
    }
}

# test for delete
# PARAMS = {
#     "app": APPID,
#     "ids": [2]
# }

def post_todo(params):
    headers={"X-Cybozu-API-Token":API_TOKEN,"Content-Type":"application/json"}
    resp=requests.post(URL+"record.json",json=params,headers=headers)

    return resp

def get_todo():
    headers={"X-Cybozu-API-Token":API_TOKEN}
    params = {"app": APPID}
    resp = requests.get(URL + "records.json", headers=headers, params=params)

    return resp.json()

def put_start_time(params):
    headers={"X-Cybozu-API-Token":API_TOKEN,"Content-Type":"application/json"}
    resp=requests.put(URL+"record.json", json=params, headers=headers)

    return resp.json()

def delete_todo(params):
    headers={"X-Cybozu-API-Token":API_TOKEN,"Content-Type":"application/json"}
    resp=requests.delete(URL+"records.json", json=params, headers=headers)

    return resp.json()

# if __name__=="__main__":
    # POST
    # resp=post_todo(PARAMS)
    # print(resp.text)

    # GET
    # resp = get_todo()
    # print(resp)
    # if resp.status_code == 200:
    #     data = resp.json()
    #     records = data.get("records", [])
    #     for record in records:
    #         task = record.get("task", {}).get("value", "")
    #         time = record.get("time", {}).get("value", "")
    #         worker = record.get("worker", {}).get("value", "")
    #         print("Task:", task)
    #         print("Time:", time)
    #         print("Worker:", worker)
    #         print("--------------------")
    # else:
    #     print("Error:", resp.status_code)

    # PUT
    # resp = put_start_time(PARAMS)
    # print(PARAMS)
    # print(resp)

    # DELETE
    # resp = delete_todo(PARAMS)
    # print(resp)

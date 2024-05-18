from dotenv import load_dotenv
load_dotenv()

import os
import requests

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
    "id": 2,
    "record": {
        "startTime": {
            "value": "2024-05-18T23:05+09:00"
        }
    }
}

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

    return resp

if __name__=="__main__":
    # POST
    # resp=post_todo(PARAMS)
    # print(resp.text)

    # GET
    # resp = get_todo()
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
    resp = put_start_time(PARAMS)
    print(resp)
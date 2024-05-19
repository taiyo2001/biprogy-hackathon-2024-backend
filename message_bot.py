import json, os, logging, requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
from db_session import line_authenticate
from client_session import todo_get
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextSendMessage
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
import asyncio

app = FastAPI()
scheduler = AsyncIOScheduler()
access_token = os.getenv("CHANNEL_ACCESS_TOKEN")

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not scheduler.running:
        scheduler.start()
        scheduler.add_job(send_line_notifications_for_troubles, 'interval', args=[access_token], seconds=15)
    yield

secret = os.getenv("CHANNEL_SECRET")

async def send_line_notifications_for_troubles(access_token: str):
    todos = await todo_get()
    line_messages = []

    for todo in todos:
        hours, minutes = divmod(todo['over_time'], 60)

        if hours > 0:
            over_time_text = f"{hours}時間{minutes}分"
        else:
            over_time_text = f"{minutes}分"

        if todo['trouble_level'] == 6 | todo['trouble_level'] == 7:
            trouble_level_text = "低"
        elif todo['trouble_level'] == 8 | todo['trouble_level'] == 9:
            trouble_level_text = "中"
        elif todo['trouble_level'] == 10:
            trouble_level_text = "高"
        else:
            continue 

        message_text = f"{todo['worker']}さんの「{todo['task']}」が終わっていません！\n{over_time_text}オーバーしています！\nトラブルレベル：{trouble_level_text}"
        line_messages.append({"type": "text", "text": message_text})

    if line_messages:
        send_line_notification(line_messages, access_token)

    return {"message": "Notifications sent if any trouble level was above 6"}

def send_line_notification(messages, access_token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "messages": messages
    }
    try:
        response = requests.post("https://api.line.me/v2/bot/message/broadcast", headers=headers, json=data)

        if response.status_code == 200:
            return {
                "status": "success",
                "message": "Message sent successfully",
                "data": response.json()
            }
        else:
            return {
                "status": "error",
                "message": "Failed to send message",
                "error": response.json()
            }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": "Request failed",
            "error": str(e)
        }
    

async def main():
    async with lifespan(app):
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=3002, reload=True)
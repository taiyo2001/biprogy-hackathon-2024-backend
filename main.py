from fastapi import FastAPI
from client_session import app as client_app

app = FastAPI()

# client_app のルートを含める
app.mount("/", client_app)

# アプリケーションの起動コード
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=3001, reload=True)
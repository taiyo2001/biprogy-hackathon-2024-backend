from fastapi import FastAPI
from client_session import app as client_app
from client_session_qa import app as qa_app
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # 認証情報のアクセスを許可(今回は必要ない)
    allow_credentials=True,
    # 全てのリクエストメソッドを許可(["GET", "POST"]など個別指定も可能)
    allow_methods=["*"],
    # アクセス可能なレスポンスヘッダーを設定（今回は必要ない）
    allow_headers=["*"],
)

# client_app のルートを含める
app.mount("/", client_app)
app.mount("/lll", qa_app)

# アプリケーションの起動コード
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=3001, reload=True)
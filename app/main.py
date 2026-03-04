from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Fashion AI Chatbot")

class ChatRequest(BaseModel):
    session_id: str
    user_id: str | None = None
    message: str

class ChatResponse(BaseModel):
    reply: str
    next_state: str | None = None


@app.get("/")
def root():
    return {"message": "Fashion AI Chatbot Server Running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat/message", response_model=ChatResponse)
def chat_message(req: ChatRequest):

    user_msg = req.message.lower()

    # 간단한 intent 분기 (MVP)
    if "환불" in user_msg or "교환" in user_msg:
        return ChatResponse(
            reply="환불/교환을 진행하시려면 주문번호를 입력해주세요.",
            next_state="RETURN_FLOW"
        )

    elif "추천" in user_msg or "옷" in user_msg:
        return ChatResponse(
            reply="어떤 스타일을 찾고 계신가요? (예: 검정 오버핏 후드)",
            next_state="SHOP_SEARCH"
        )

    else:
        return ChatResponse(
            reply="무엇을 도와드릴까요? (상품추천 / 교환 / 환불)",
            next_state=None
        )
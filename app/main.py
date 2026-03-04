from fastapi import FastAPI
from pydantic import BaseModel

from app.products import PRODUCTS
from app.search import extract_filters, search_products

app = FastAPI(title="Fashion AI Chatbot")

class ChatRequest(BaseModel):
    session_id: str
    user_id: str | None = None
    message: str

class ChatResponse(BaseModel):
    reply: str
    next_state: str | None = None
    recommended_products: list | None = None


@app.get("/")
def root():
    return {"message": "Fashion AI Chatbot Server Running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat/message", response_model=ChatResponse)
def chat_message(req: ChatRequest):
    user_msg = req.message.strip()

    # 1) 환불/교환 intent
    if "환불" in user_msg or "교환" in user_msg:
        return ChatResponse(
            reply="환불/교환을 진행하시려면 주문번호를 입력해주세요.",
            next_state="RETURN_FLOW",
            recommended_products=None,
        )

    # 2) 상품 추천 intent (Day2: 룰 기반 검색)
    filters = extract_filters(user_msg)
    results = search_products(PRODUCTS, filters)

    if results:
        top = results[:5]
        lines = ["조건에 맞는 상품을 찾았어 👇"]
        for p in top:
            lines.append(f"- [{p['brand']}] {p['name']} / {p['color']} / {p['price']:,}원 (id={p['id']})")

        return ChatResponse(
            reply="\n".join(lines),
            next_state="SHOP_SEARCH",
            recommended_products=top,
        )

    return ChatResponse(
        reply="원하는 조건을 더 알려줘! 예) '검정 오버핏 후드 5만원 이하' 처럼 👍",
        next_state="SHOP_SEARCH",
        recommended_products=[],
    )
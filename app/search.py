# app/search.py
from typing import List, Dict

COLOR_MAP = {
    "검정": "black",
    "블랙": "black",
    "black": "black",
    "하양": "white",
    "화이트": "white",
    "white": "white",
    "아이보리": "ivory",
    "오프화이트": "ivory",
    "ivory": "ivory",
}

CATEGORY_KEYWORDS = {
    "후드": "hoodie",
    "후드티": "hoodie",
    "후드티셔츠": "hoodie",
    "후드집업": "hoodie",
    "슬랙스": "slacks",
    "셔츠": "shirt",
}

def extract_filters(text: str) -> Dict[str, str]:
    """아주 단순한 룰 기반 필터 추출 (Day2 용)"""
    t = text.lower()

    color = None
    for k, v in COLOR_MAP.items():
        if k.lower() in t:
            color = v
            break

    category = None
    for k, v in CATEGORY_KEYWORDS.items():
        if k.lower() in t:
            category = v
            break

    return {"color": color, "category": category}

def search_products(products: List[dict], filters: Dict[str, str]) -> List[dict]:
    """필터 조건에 맞는 상품 검색"""
    results = []
    for p in products:
        ok = True
        if filters.get("color") and p["color"] != filters["color"]:
            ok = False
        if filters.get("category") and p["category"] != filters["category"]:
            ok = False
        if ok:
            results.append(p)
    return results
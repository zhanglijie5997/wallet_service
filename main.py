# main.py
from fastapi import FastAPI
from models.res_mode import ApiResponse
from pydantic import BaseModel

app = FastAPI(
    title="我的第一个 FastAPI 项目",
    version="0.0.1",
    description="2026年新手入门示例",
)

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

@app.get("/", response_model=ApiResponse[list[dict]])
async def read_root():
    return ApiResponse(data=[], code=10000)

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
async def create_item(item: Item):
    return {"item_name": item.name, "price_with_tax": item.price * 1.1}
from pydantic import BaseModel


class HomeModel(BaseModel):
    name: str
    age: int
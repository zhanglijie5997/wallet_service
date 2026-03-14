from typing import TypeVar
from pydantic import BaseModel
from typing import Any, Optional, TypeVar, Generic

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    code: int = 200
    msg: str = "success"
    data: Optional[T] = None


def success(data: Any = None, msg: str = "success", code: int = 200):
    return ApiResponse(code=code, msg=msg, data=data)

def fail(msg: str, code: int = 40000, data: Any = None):
    return ApiResponse(code=code, msg=msg, data=data)
from enum import Enum, auto, unique
from typing import TypeVar
from pydantic import BaseModel
from typing import Any, Optional, TypeVar, Generic

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    code: int = 200
    msg: str = "success"
    data: Optional[T] = None


# 状态枚举
@unique  # 防止值重复（强烈推荐生产环境加这个）
class Status(Enum):
    SUCCESS = auto()
    FAIL = auto()
    TIMEOUT = auto()
    SYSTEMERROR = auto()

    @property
    def display(self) -> str:
        return {
            Status.SUCCESS: "成功",
            Status.FAIL: "失败",
            Status.TIMEOUT: "请求超时",
            Status.SYSTEMERROR: "系统错误",
        }[self]
    @property
    def default_code(self) -> int:
        """枚举对应的推荐 HTTP/业务状态码"""
        return {
            Status.SUCCESS:     1200,
            Status.FAIL:        1300,
            Status.TIMEOUT:     1408,
            Status.SYSTEMERROR: 1500,
        }[self]

def success(
    data:Optional[T] = None, msg: str = Status.SUCCESS.display, code: int = Status.SUCCESS.default_code
):
    return ApiResponse(code=code, msg=msg, data=data)


def fail(msg: str, code: int = 40000, data: Any = None):
    return ApiResponse(code=code, msg=msg, data=data)

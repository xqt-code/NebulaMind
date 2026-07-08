from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ResponseModel(BaseModel, Generic[T]):
    """统一响应模型

    所有 API 接口统一使用此模型返回数据，确保前端能按统一格式解析响应。
    """

    code: int
    msg: str
    data: Optional[T] = None

    @staticmethod
    def success(data: Optional[T] = None) -> "ResponseModel[T]":
        """成功响应，默认 code=200, msg="操作成功" """
        return ResponseModel(code=200, msg="操作成功", data=data)

    @staticmethod
    def error(code: int, msg: str) -> "ResponseModel":
        """失败响应，需传入错误码和错误信息"""
        return ResponseModel(code=code, msg=msg, data=None)
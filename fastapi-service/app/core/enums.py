from enum import Enum


class ErrorCodeEnum(Enum):
    """业务错误码枚举"""

    SUCCESS = (200, "操作成功")
    PARAM_ERROR = (400, "参数错误")
    UNAUTHORIZED = (401, "未授权")
    FORBIDDEN = (403, "禁止访问")
    NOT_FOUND = (404, "资源不存在")
    BUSINESS_ERROR = (500, "业务异常")
    SYSTEM_ERROR = (500, "系统错误")

    @property
    def code(self) -> int:
        return self.value[0]

    @property
    def msg(self) -> str:
        return self.value[1]
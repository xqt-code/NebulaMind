import traceback

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.enums import ErrorCodeEnum
from app.core.response import ResponseModel
from app.utils.trace_id_util import get_trace_id


class BusinessException(Exception):
    """业务异常

    用于在业务逻辑中主动抛出，包含错误码和错误信息。
    """

    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg
        super().__init__(msg)


def register_exception_handlers(app) -> None:
    """注册全局异常处理器"""

    @app.exception_handler(BusinessException)
    async def business_exception_handler(request: Request, exc: BusinessException):
        """业务异常处理"""
        trace_id = get_trace_id()
        return JSONResponse(
            status_code=exc.code if exc.code < 500 else 500,
            content=ResponseModel.error(
                code=exc.code,
                msg=f"[TraceID: {trace_id}] {exc.msg}",
            ).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """请求参数校验异常处理"""
        trace_id = get_trace_id()
        error_detail = exc.errors() if hasattr(exc, "errors") else str(exc)
        return JSONResponse(
            status_code=ErrorCodeEnum.PARAM_ERROR.code,
            content=ResponseModel.error(
                code=ErrorCodeEnum.PARAM_ERROR.code,
                msg=f"[TraceID: {trace_id}] 参数校验失败: {error_detail}",
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """全局未知异常处理，打印完整堆栈"""
        trace_id = get_trace_id()
        traceback.print_exc()
        return JSONResponse(
            status_code=ErrorCodeEnum.SYSTEM_ERROR.code,
            content=ResponseModel.error(
                code=ErrorCodeEnum.SYSTEM_ERROR.code,
                msg=f"[TraceID: {trace_id}] 系统内部错误: {str(exc)}",
            ).model_dump(),
        )
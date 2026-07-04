from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.constants import TRACE_ID_HEADER
from app.utils.trace_id_util import (
    generate_trace_id,
    get_trace_id,
    set_trace_id,
)


class TraceIDMiddleware(BaseHTTPMiddleware):
    """TraceID 中间件

    从请求头 X-Trace-ID 获取 TraceID，若不存在则自动生成。
    将 TraceID 注入到 contextvars 和 request.state 中，并在响应头中返回。
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        # 从请求头获取 TraceID，没有则生成新的
        trace_id = request.headers.get(TRACE_ID_HEADER, "")
        if not trace_id:
            trace_id = generate_trace_id()

        # 存储到 contextvars（供日志、工具层使用）
        set_trace_id(trace_id)

        # 存储到 request.state（供路由层使用）
        request.state.trace_id = trace_id

        # 继续处理请求
        response = await call_next(request)

        # 将 TraceID 注入到响应头
        response.headers[TRACE_ID_HEADER] = trace_id

        return response
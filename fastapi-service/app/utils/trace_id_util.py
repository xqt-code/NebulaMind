import uuid
from contextvars import ContextVar

# 全局上下文变量，用于在当前请求链路中传递 TraceID
trace_id_context: ContextVar[str] = ContextVar("trace_id", default="")


def get_trace_id() -> str:
    """获取当前请求的 TraceID"""
    return trace_id_context.get()


def set_trace_id(trace_id: str) -> None:
    """设置当前请求的 TraceID"""
    trace_id_context.set(trace_id)


def generate_trace_id() -> str:
    """生成新的 TraceID（UUID 格式）"""
    return str(uuid.uuid4())
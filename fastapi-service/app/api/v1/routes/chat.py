# ============================================================================
# 1. 导入依赖
# ============================================================================
# FastAPI 核心组件
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

# Pydantic 数据校验（定义请求/响应结构）
from pydantic import BaseModel, Field

# 类型注解
from typing import Optional, Dict, Any

# 日志
from app.utils.logger import get_logger

# 统一响应构建器（确保响应格式一致）
from app.core.response_builder import ResponseBuilder

# 业务服务层（RAG 服务）
from app.services.rag_service import RagService

# 创建日志记录器
logger = get_logger(__name__)

# ============================================================================
# 2. 定义路由对象
# ============================================================================
# 创建一个 APIRouter 实例，所有接口以 /chat 为前缀
# tags 用于在 Swagger 文档中分组
router = APIRouter(prefix="/chat", tags=["智能问答"])

# ============================================================================
# 3. 定义请求体模型（Pydantic）
# ============================================================================
class AskRequest(BaseModel):
    """
    问答请求体
    - question: 用户问题（必填，长度至少 1）
    - tenant_id: 租户 ID（可选，默认为 "1"）
    - stream: 是否流式返回（暂时保留，后续扩展）
    """
    question: str = Field(..., min_length=1, description="用户问题")
    tenant_id: Optional[str] = Field(default="1", description="租户 ID")
    stream: bool = Field(default=False, description="是否流式返回（暂未实现）")

    # 示例数据（用于 Swagger 文档展示）
    class Config:
        json_schema_extra = {
            "example": {
                "question": "RAG 和长上下文有什么区别？",
                "tenant_id": "1",
                "stream": False
            }
        }

# ============================================================================
# 4. 初始化业务服务（依赖注入）
# ============================================================================
# 创建 RagService 实例，在请求处理中复用
# 注意：这里我们直接实例化了，更规范的写法是用 Depends 注入
# 但为了简单清晰，我们先直接创建
rag_service = RagService()

# ============================================================================
# 5. 核心接口：问答
# ============================================================================
@router.post(
    "/ask",
    response_model=Dict[str, Any],  # 返回任意字典（由 ResponseBuilder 保证格式统一）
    summary="智能问答",
    description="基于 RAG 的企业内部知识库问答，支持引用溯源"
)
async def ask_question(request: AskRequest):
    """
    处理用户问答请求

    流程：
        1. 记录请求日志
        2. 调用 RagService.ask() 执行完整 RAG 流程
        3. 返回统一格式的 JSON 响应

    异常处理：
        - 如果服务内部异常，返回 500 错误
        - 参数校验失败会由 FastAPI 自动处理（422）
    """
    # ---- 1. 记录请求日志 ----
    logger.info(
        f"收到问答请求: question={request.question[:50]}..., "
        f"tenant={request.tenant_id}, stream={request.stream}"
    )

    try:
        # ---- 2. 调用业务层 ----
        # RagService.ask 会执行：缓存查询 → 向量检索 → Prompt 构建 → LLM 调用 → 结果缓存
        # 返回统一格式的字典（包含 answer、references、confidence、has_answer）
        result = rag_service.ask(
            question=request.question,
            tenant_id=request.tenant_id
        )

        # ---- 3. 返回成功响应 ----
        # 注意：result 已经是 ResponseBuilder 构建好的格式，直接返回 JSONResponse
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=result
        )

    except Exception as e:
        # ---- 4. 异常处理（兜底） ----
        # 捕获所有未预料的异常，记录日志，返回 500
        logger.error(f"问答处理异常: {e}", exc_info=True)
        # 使用 ResponseBuilder 统一构建错误响应
        error_response = ResponseBuilder.error(str(e))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response
        )

# ============================================================================
# 6. 可选接口：健康检查（用于调试）
# ============================================================================
@router.get(
    "/health",
    summary="问答服务健康检查",
    description="检查问答服务是否可用"
)
async def chat_health():
    """
    简单的健康检查端点，确认服务是否正常运行
    """
    return {
        "status": "ok",
        "service": "chat",
        "rag_loaded": rag_service.vector_store is not None
    }
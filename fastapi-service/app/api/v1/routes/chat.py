"""
chat.py - 智能问答路由

【职责】
- 定义 URL 路径（/api/v1/chat/ask）
- 接收 HTTP 请求，提取参数
- 调用业务层（ChatService）
- 返回 JSON 响应
- 以同步或流式方式返回结果

【不做什么】
- 不写业务逻辑
- 不直接调用数据层

【依赖】
- RagService：核心 RAG 逻辑（待实现）
- 请求/响应模型：Pydantic 定义
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
import uuid

from app.services.rag_service import RagService
from app.services.chat_service import ChatService
from app.core.response import ResponseModel
from app.utils.logger import get_logger

# 导入 RAG 服务（后续实现）
from app.services.rag_service import RagService
from app.core.response import ResponseModel
from app.utils.logger import get_logger

logger = get_logger(__name__)


# =============================================================================
# 1. 定义路由
# =============================================================================
router = APIRouter(prefix="/chat", tags=["智能问答"])

# =============================================================================

# 2. 定义请求/响应模型（Pydantic）
# =============================================================================
class AskRequest(BaseModel):
    """问答请求体"""
    question: str                     # 用户问题
    tenant_id: Optional[str] = "1"    # 租户 ID（多租户隔离）
    conversation_id: Optional[str] = None  # 会话 ID（多轮对话）
    stream: bool = False              # 是否流式返回

class AskResponse(BaseModel):
    """问答响应体（非流式）"""
    answer: str
    references: List[Dict[str, Any]]
    conversation_id: str
    confidence: float
    has_answer: bool


# =============================================================================
# 3. 初始化 RAG 服务（单例，全局复用）
# =============================================================================
# 创建业务层实例（依赖注入）
chat_service = ChatService()

# =============================================================================
# 4. 核心接口
# =============================================================================
@router.post("/ask")
async def ask_question(request: AskRequest):
    """
    智能问答接口

    【流程】
    1. 记录日志（便于追踪）
    2. 调用业务层（ChatService）
    3. 封装统一响应返回

    支持两种模式：
    - stream=False：返回完整 JSON（适合简单场景）
    - stream=True：返回 SSE 流式数据（适合实时打字效果）

    工作流程：
    1. 校验参数
    2. 调用 RagService 执行完整 RAG 流程
    3. 根据 stream 参数选择返回方式
    """
    logger.info(
        f"收到问答请求: question={request.question[:50]}, "
        f"tenant={request.tenant_id}, stream={request.stream}"
    )

    # ---- 步骤 1：参数校验 ----
    if not request.question or len(request.question.strip()) == 0:
        raise HTTPException(status_code=400, detail="问题不能为空")

    # ---- 步骤 2：生成或复用会话 ID ----
    conversation_id = request.conversation_id or str(uuid.uuid4())

    # ---- 步骤 3：调用 Chat 服务 ----
    result = chat_service.ask(
        question=request.question,
        tenant_id=request.tenant_id
    )

    # 封装统一响应
    return ResponseModel.success(data=result)


# =============================================================================
# 5. 可选的额外接口：健康检查
# =============================================================================
@router.get("/health")
async def chat_health():
    """检查聊天服务是否可用"""
    return ResponseModel.success(data={"status": "ok", "service": "chat"})



'''
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List

from app.core.response import ResponseModel
from app.models.request import AskRequest



router = APIRouter(prefix="/chat", tags=["智能问答"])

class AskRequest(BaseModel):
    question: str
    tenant_id: str = "1"

@router.post("/ask")
async def ask_question(request: AskRequest):
    """智能问答接口 - SSE 流式返回"""
    async def generate():
        # 这里调用 RAG 服务，逐 token 返回
        async for chunk in rag_service.ask_stream(request.question, request.tenant_id):
            yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"
    
    """TODO: 调用 rag_service.ask() 实现完整的 RAG 问答流程

    RAG 全流程说明：
    1. 【缓存查询】调用 cache_service.get_similar_question()
       - 检查是否有历史相似问题的缓存答案
       - 命中缓存直接返回，避免 LLM 调用

    2. 【向量检索】调用 embedding_service.embed() + vector_service.search()
       - 将用户问题转为向量
       - 在向量库中检索 Top-K 相关文档片段

    3. 【重排序】调用 rerank_service.rerank()
       - 对粗排结果进行精排（Cross-Encoder）
       - 取 Top-N 最相关文档

    4. 【Prompt 构建】组装 system_prompt + context + user question
       - 将检索到的文档片段作为上下文注入 Prompt
       - 设定角色、输出格式等约束

    5. 【LLM 调用】调用 llm_service.chat()
       - 使用通义千问大模型生成回答
       - 支持 JSON Mode 结构化输出

    6. 【结果缓存】调用 cache_service.set_cache()
       - 将问答对存入语义缓存
       - 为后续相似问题提供快速命中

    面试讲：RAG 的三个核心挑战：
    - 怎么召回得准（Embedding 质量 + 检索策略）
    - 怎么重排得好（Reranker 精排）
    - 怎么控制成本（语义缓存 + 多级缓存）
    """
    # TODO: 实现 RAG 问答流程
    return ResponseModel.success(
        data={
            "answer": "RAG 问答功能待实现",
            "references": [],
            "conversation_id": request.conversation_id or "new",
            "confidence": 0.0,
            "has_answer": False,
        }
    )
'''
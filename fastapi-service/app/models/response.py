from typing import List, Optional

from pydantic import BaseModel


class AskResponse(BaseModel):
    """智能问答响应模型"""

    answer: str
    references: List[dict]
    conversation_id: str
    confidence: float
    has_answer: bool


class DocumentProcessResponse(BaseModel):
    """文档处理响应模型"""

    task_id: str
    status: str
    message: str
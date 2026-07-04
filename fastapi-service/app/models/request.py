from typing import Optional

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    """智能问答请求模型"""

    question: str = Field(
        ...,
        min_length=1,
        description="用户提问内容，不能为空",
    )
    tenant_id: Optional[str] = Field(
        default=None,
        description="租户ID，用于多租户数据隔离",
    )
    conversation_id: Optional[str] = Field(
        default=None,
        description="会话ID，用于多轮对话上下文关联",
    )
    stream: bool = Field(
        default=False,
        description="是否开启流式输出",
    )


class DocumentProcessRequest(BaseModel):
    """文档处理请求模型"""

    file_name: str = Field(
        ...,
        description="文档文件名",
    )
    file_content: str = Field(
        ...,
        description="文档文本内容",
    )
    tenant_id: str = Field(
        ...,
        description="租户ID，指定文档归属的租户",
    )
    document_id: str = Field(
        ...,
        description="文档唯一标识ID",
    )
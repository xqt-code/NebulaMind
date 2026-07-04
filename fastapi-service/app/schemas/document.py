from typing import Dict, List, Optional

from pydantic import BaseModel


class DocumentSchema(BaseModel):
    """文档数据模型

    用于服务层内部数据传递，包含文档内容、向量嵌入及元数据。
    """

    id: str
    document_id: str
    file_name: str
    content: str
    embedding: List[float]
    metadata: Dict
    similarity: Optional[float] = None
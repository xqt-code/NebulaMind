"""
response_builder.py - 统一响应构建器

职责：
- 封装 RAG 问答的返回格式
- 统一处理成功、降级、失败三种场景的日志和返回结构
- 让业务代码（rag_service、chat_service）保持干净
"""

from typing import List, Dict, Any, Optional
from app.utils.logger import get_logger

logger = get_logger(__name__)

class ResponseBuilder:
    pass
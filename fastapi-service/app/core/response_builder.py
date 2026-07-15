# ============================================================================
# 1. 导入依赖
# ============================================================================
from typing import Dict, Any, List, Optional

# 导入日志记录器，用于记录构建响应过程中的事件
from app.utils.logger import get_logger

# 创建当前模块的日志记录器
logger = get_logger(__name__)

# ============================================================================
# 2. 核心类：统一响应构建器
# ============================================================================
class ResponseBuilder:
    """
    统一响应构建器（企业级响应格式）

    职责：
        1. 确保所有 API 返回的 JSON 格式完全一致
        2. 提供成功、降级、错误三种场景的响应构建方法
        3. 记录日志，便于追踪响应生成过程

    使用方式：
        # 成功场景
        ResponseBuilder.success(answer="...", references=[...])
        # 降级场景（向量库不可用等）
        ResponseBuilder.fallback(answer="...", reason="向量库未加载")
        # 错误场景（API 调用失败等）
        ResponseBuilder.error(error_msg="...")

    返回格式（所有方法统一）：
        {
            "answer": "...",
            "references": [...],
            "confidence": 0.0,
            "has_answer": True/False
        }

    设计原则：
        - 单一职责：只做响应构建，不包含业务逻辑
        - 开闭原则：新增场景时不需要修改已有代码
        - 日志规范：每个响应构建都有对应的日志记录
    """

    @staticmethod
    def success(answer: str, references: List[Dict[str, Any]], confidence: float, latency_ms: int = 0, token_usage: dict = None) -> Dict[str, Any]:
        """
        构建成功响应

        适用场景：
            - RAG 检索成功并生成了回答
            - 纯对话成功返回了回答
            - 任何业务逻辑正常完成的场景

        参数:
            answer: 回答内容（字符串）
            references: 引用来源列表，每个元素包含：
                - file_name: 文件名
                - content: 引用内容片段
                - similarity: 相似度分数
            confidence: 置信度（0-1 之间的浮点数，默认 0.8）

        返回:
            Dict[str, Any]: 统一格式的响应字典

        示例:
            >>> ResponseBuilder.success(
                    answer="RAG 是检索增强生成...",
                    references=[{"file_name": "doc.md", "content": "...", "similarity": 0.9}],
                    confidence=0.85
                )
            {
                "code": 200,
                "msg": "操作成功",
                "data": {
                    "answer": "RAG 是检索增强生成...",
                    "references": [...],
                    "confidence": 0.85,
                    "has_answer": True
                }
            }
        """
        # ---- 1. 记录日志 ----
        logger.info(
            f"构建成功响应: 回答长度={len(answer)}, 引用数量={len(references)}, "
            f"置信度={confidence}"
        )

        # ---- 2. 构建返回体 ----
        # 数据部分：包含业务数据
        data = {
            "answer": answer,
            "references": references,
            "confidence": confidence,
            "has_answer": True,
            "latency_ms": latency_ms,  # 🔥 关键：前端要读这个字段
            "token_usage": token_usage or {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }

        # 外层包装：统一响应格式
        return {
            "code": 200,
            "msg": "操作成功",
            "data": data,
        }

    @staticmethod
    def fallback(answer: str, reason: str = "降级响应") -> Dict[str, Any]:
        """
        构建降级响应

        适用场景：
            - 向量库未加载（服务启动了但没有文档数据）
            - 向量检索无结果（用户问的问题不在知识库里）
            - 任何需要跳过 RAG 检索，直接用纯对话的场景

        参数:
            answer: 降级回答内容（通常来自纯对话模式）
            reason: 降级原因（用于日志记录，便于排查问题）

        返回:
            Dict[str, Any]: 统一格式的响应字典

        示例:
            >>> ResponseBuilder.fallback(
                    answer="抱歉，知识库中未找到相关内容。",
                    reason="向量检索无结果"
                )
            {
                "code": 200,
                "msg": "操作成功",
                "data": {
                    "answer": "抱歉，知识库中未找到相关内容。",
                    "references": [],
                    "confidence": 0.0,
                    "has_answer": True
                }
            }
        """
        # ---- 1. 记录日志（包含降级原因） ----
        logger.warning(
            f"构建降级响应: 回答长度={len(answer)}, 原因={reason}"
        )

        # ---- 2. 构建返回体 ----
        data = {
            "answer": answer,
            "references": [],          # 降级模式没有引用来源
            "confidence": 0.0,          # 降级模式没有置信度评分
            "has_answer": True,         # 仍然返回了回答，只是没有检索
        }

        return {
            "code": 200,
            "msg": "操作成功",
            "data": data,
        }

    @staticmethod
    def error(error_msg: str) -> Dict[str, Any]:
        """
        构建错误响应

        适用场景：
            - 大模型 API 调用失败（通义千问连接超时、网络错误）
            - 系统内部异常（代码报错、依赖缺失）
            - 任何导致无法返回正常回答的情况

        参数:
            error_msg: 错误信息（字符串，用于日志记录和调试）

        返回:
            Dict[str, Any]: 统一格式的错误响应字典

        示例:
            >>> ResponseBuilder.error("连接通义千问API超时")
            {
                "code": 500,
                "msg": "[TraceID: xxx] 系统内部错误: 连接通义千问API超时",
                "data": {
                    "answer": "抱歉，AI 服务暂时不可用，请稍后再试。",
                    "references": [],
                    "confidence": 0.0,
                    "has_answer": False
                }
            }

        设计考虑：
            - 不暴露内部错误细节给前端（避免安全风险）
            - 但仍然记录完整错误到日志（便于运维排查）
            - 返回友好的用户提示
        """
        # ---- 1. 记录错误日志（包含完整信息，方便排查） ----
        logger.error(
            f"构建错误响应: 错误信息={error_msg}"
        )
        # 使用 exc_info=True 会打印完整堆栈，方便调试
        # 但在生产环境可以去掉，避免日志过多
        logger.error(f"详细错误堆栈: ", exc_info=True)

        # ---- 2. 构建返回体 ----
        data = {
            "answer": "抱歉，AI 服务暂时不可用，请稍后再试。",
            "references": [],          # 错误模式没有引用
            "confidence": 0.0,          # 错误模式没有置信度
            "has_answer": False,        # 明确标识没有有效回答
        }

        # ---- 3. 构建错误响应 ----
        # 注意：这里返回 500 状态码对应的内部错误，但外层由 HTTP 状态码控制
        # 这里保留 500，让调用方（如 chat.py）根据情况转成 HTTP 500
        return {
            "code": 500,
            "msg": f"系统内部错误: {error_msg}",
            "data": data,
        }

    @staticmethod
    def from_exception(e: Exception) -> Dict[str, Any]:
        """
        从异常对象构建错误响应（便捷方法）

        适用场景：
            - 捕获到 Exception 时直接调用，不需要手动提取 error_msg

        参数:
            e: 异常对象（Exception 或其子类）

        返回:
            Dict[str, Any]: 统一格式的错误响应字典

        示例:
            >>> try:
            ...     # some code
            ... except Exception as e:
            ...     return ResponseBuilder.from_exception(e)
        """
        return ResponseBuilder.error(str(e))

    @staticmethod
    def is_success(response: Dict[str, Any]) -> bool:
        """
        判断响应是否为成功响应（工具方法）

        适用场景：
            - 前端判断响应状态
            - 服务间调用判断结果

        参数:
            response: 响应字典

        返回:
            bool: True 表示成功，False 表示失败
        """
        return response.get("code") == 200 and response.get("data", {}).get("has_answer", False)
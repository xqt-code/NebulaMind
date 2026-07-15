"""
llm_repository.py - 数据层（Repository）

【职责】
- 封装对通义千问 API 的调用
- 只负责：接收 prompt → 调用 API → 返回文本
- 不包含任何业务逻辑（如 Prompt 构造、异常转义等）

【被谁调用】
- 被业务层（ChatService / RagService）调用

【为什么要有这一层？】
- 解耦：业务层不需要知道 API 调用的细节（密钥、端点、重试等）
- 可替换：将来换大模型，只改这一个文件
"""

import dashscope
from dashscope import Generation
from app.core.config import settings
from app.utils.logger import get_logger
# 在文件顶部确认已经导入了时间模块（用于后面的 Latency 计算）
import time

logger = get_logger(__name__)


class LLMRepository:
    """大模型数据仓库"""

    def __init__(self):
        # 从全局配置中读取 API Key 和模型名称（由 config.py 从 .env.dev 加载）
        self.api_key = settings.dashscope_api_key
        self.model = settings.llm_model or "qwen-plus"

        # 设置 dashscope 的 API Key（全局生效）
        dashscope.api_key = self.api_key

        logger.info(f"LLM 数据仓库初始化完成，模型: {self.model}")

    def chat(self, prompt: str, system_prompt: str = None) -> str:
        """
        调用通义千问 API
        返回格式：{"content": "...", "prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

        【参数】
        - prompt: 用户的问题（必填）
        - system_prompt: 系统指令（可选，用于设定 AI 的角色）

        【返回】
        - AI 的回答文本（字符串）

        【异常】
        - 如果 API 调用失败，抛出异常（由上层业务层捕获处理）
        """
        # 1. 构造消息列表（通义千问 API 要求的格式）
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = Generation.call(
                model=self.model,
                messages=messages,
                result_format="message",
                temperature=0.2,
            )

            if response.status_code == 200:
                content = response.output.choices[0].message.content
                usage = response.usage  # dashscope 返回的用量字典
                logger.info(f"API 调用成功，回答长度: {len(content)} 字符")

                # 🔥 返回字典，而不是纯字符串
                return {
                    "content": content,
                    "prompt_tokens": usage.get("input_tokens", 0),
                    "completion_tokens": usage.get("output_tokens", 0),
                    "total_tokens": usage.get("total_tokens", 0)
                }
            else:
                logger.error(f"API 调用失败: {response.code} - {response.message}")
                raise Exception(f"大模型 API 错误: {response.message}")

        except Exception as e:
            logger.error(f"API 调用异常: {e}")
            raise
"""
chat_service.py - 业务层（Service）

【职责】
- 接收 Controller 传来的用户问题
- 组装 System Prompt（定义 AI 角色）
- 调用数据层（LLMRepository）获取回答
- 把结果整理成统一格式返回给 Controller

【承上】
- 被 Controller 调用，接收用户问题

【启下】
- 调用数据层（LLMRepository），获取大模型回答

【为什么要有这一层？】
- 业务逻辑集中管理，不散落在 Controller 里
- 后续可扩展（如添加敏感词过滤、对话历史保存等）
"""

# typing: 用于类型注解（告诉调用方这个函数返回什么类型）
from typing import Dict, Any

# logger: 用于打印日志（调试时能看见每一步的执行情况）
from app.utils.logger import get_logger

# ResponseBuilder: 统一响应构建器（负责把结果包装成统一格式）
from app.core.response_builder import ResponseBuilder

# LLMRepository: 负责调用大模型 API（通义千问）
from app.repositories.llm_repository import LLMRepository

# 创建日志记录器，用于打印此模块的信息
logger = get_logger(__name__)


class ChatService:
    """纯对话业务服务（不带知识库检索）

    职责：
    - 接收用户问题
    - 构建
    System
    Prompt（定义
    AI
    的角色和行为）
    - 直接调用大模型（LLM）生成回答
    - 返回统一格式的响应

    适用场景：
    - 通用问答
    - 闲聊
    - 不需要检索企业内部文档的场景
    """

def __init__(self):
    # 依赖数据层（依赖注入）
    self.llm_repo = LLMRepository()
    logger.info("ChatService 初始化完成（纯对话模式）")

def ask(self, question: str, tenant_id: str = "1") -> Dict[str, Any]:
    """
        处理用户问题，返回 AI 回答

        参数:
            question: 用户问题（字符串）
            tenant_id: 租户 ID（多租户场景用，目前固定为 "1"）

        返回:
            统一格式的字典，包含 answer、references、confidence、has_answer
    """

    # 1. 记录日志，方便追踪
    logger.info(f"ChatService 收到问题: {question[:30]}..., tenant={tenant_id}")

        # ============================================================
        # 2. 定义 System Prompt（设定 AI 的角色和行为规则）
             # System Prompt 的作用：
             #   - 告诉模型“你是谁”（角色设定）
             #   - 告诉模型“你能做什么、不能做什么”（能力边界）
             #   - 告诉模型“输出格式是什么”（结构化输出）
             # 这是 Prompt Engineering 的核心，用自然语言控制模型行为
        # ============================================================
    system_prompt = """
你是 NebulaMind，一个专业、友好的 AI 助手。

【规则】
- 回答准确、简洁、有条理
- 用中文回答
- 不知道就说不知道，不编造
- 适当分段，让内容清晰易读
"""

    try:
        # 3. 调用大模型（通义千问）
        # 参数说明：
        #   - prompt: 用户问题（必填）
        #   - system_prompt: 系统指令（可选，用于设定 AI 的角色）
        # 这个方法的内部实现是：
        #   1. 把 system_prompt 和 prompt 拼成符合通义千问格式的请求
        #   2. 发送 HTTP 请求到 dashscope.aliyuncs.com
        #   3. 解析返回的 JSON，提取出回答文本
        answer = self.llm_repo.chat(
            prompt = question,
            system_prompt = system_prompt,
        )

        # 4. 记录成功日志
        logger.info(f"ChatService 处理成功，回答长度: {len(answer)}")

        # 5. 构建成功响应（使用 ResponseBuilder 统一格式）
        # 纯对话模式没有引用来源，所以 references 传空数组
        # confidence 设为 0.0（因为没有检索，无法评估置信度）
        return {
            "answer": answer,
            "references": [],      # 纯对话没有引用
            "confidence": 0.0,      # 纯对话没有置信度
        }

    except Exception as e:
        # 6. 异常处理（比如 API 调用失败、网络超时等）
        logger.error(f"ChatService 处理失败: {e}")

        # 7. 构建错误响应（使用 ResponseBuilder 统一格式）
        # 这里直接调用 ResponseBuilder.error，它会返回统一的错误格式
        return ResponseBuilder.error(str(e))
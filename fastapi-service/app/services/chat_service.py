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

from app.repositories.llm_repository import LLMRepository
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ChatService:
    """纯对话业务服务"""

    def __init__(self):
        # 依赖数据层（依赖注入）
        self.llm_repo = LLMRepository()
        logger.info("ChatService 初始化完成")

    def ask(self, question: str, tenant_id: str = "1") -> dict:
        """
        处理用户问题，返回 AI 回答

        【承上】被 Controller 调用
        【启下】调用数据层获取回答

        【参数】
        - question: 用户问题
        - tenant_id: 租户 ID（多租户隔离，暂时只用默认值）

        【返回】
        - 统一格式的字典
        """
        logger.info(f"ChatService 收到问题: {question[:30]}..., tenant={tenant_id}")

        # ============================================================
        # 1. 构建 System Prompt（AI 的角色设定）
        # ============================================================
        system_prompt = """
你是 NebulaMind，一个专业、友好的 AI 助手。

【规则】
- 回答准确、简洁、有条理
- 用中文回答
- 不知道就说不知道，不编造
- 适当分段，让内容清晰易读
"""

        # ============================================================
        # 2. 调用数据层（LLMRepository）
        # ============================================================
        # 这一步就是“启下”：业务层不直接调 API，而是通过数据层
        try:
            answer = self.llm_repo.chat(question, system_prompt)

            logger.info(f"ChatService 处理成功，回答长度: {len(answer)}")

            return {
                "answer": answer,
                "references": [],      # 纯对话没有引用
                "confidence": 0.0,      # 纯对话没有置信度
                "has_answer": True,
            }

        except Exception as e:
            logger.error(f"ChatService 处理失败: {e}")
            # 返回友好错误信息，保证接口不会崩溃
            return {
                "answer": "AI 服务暂时不可用，请稍后再试。",
                "references": [],
                "confidence": 0.0,
                "has_answer": False,
            }
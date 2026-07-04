from typing import Optional

from app.models.response import AskResponse


class CacheService:
    """语义缓存服务

    基于 Redis 的语义缓存，减少重复 LLM 调用，降低成本和延迟。
    """

    def get_similar_question(
        self, question: str, tenant_id: str
    ) -> Optional[AskResponse]:
        """查询语义缓存，检查是否存在相似问题的缓存答案

        TODO: 使用 Redis 语义缓存，匹配相似问题

        技术方案：
        - 将用户问题转为向量，在 Redis 中搜索相似问题缓存
        - 使用 Redis Stack（RediSearch 模块）支持向量索引
        - 相似度阈值：余弦相似度 > 0.95 视为命中
        - 缓存 Key 设计：cache:{tenant_id}:{question_hash}

        缓存价值：
        - 降低 LLM 调用成本：大模型 API 调用是主要开销，缓存命中可节省 30%-50% 成本
        - 降低响应延迟：LLM 调用通常需要 1-3 秒，缓存命中只需毫秒级
        - 面试讲：语义缓存是 RAG 系统降本增效的核心手段，与传统的精确匹配缓存不同，
          语义缓存能识别「换种说法问同一个问题」的场景，命中率更高

        Args:
            question: 用户问题
            tenant_id: 租户ID

        Returns:
            命中缓存时返回缓存的 AskResponse，否则返回 None
        """
        # TODO: 实现语义缓存查询
        raise NotImplementedError("CacheService.get_similar_question 尚未实现")

    def set_cache(self, question: str, answer: AskResponse, tenant_id: str) -> None:
        """将问答结果存入语义缓存

        TODO: 将问题向量和答案存入 Redis

        技术方案：
        - 存储问题向量（用于相似度搜索）+ 答案 JSON
        - 设置合理的过期时间（如 1 小时），避免缓存过时
        - 面试讲：缓存过期策略需要根据业务场景调整，知识库场景通常设置 1-24 小时

        Args:
            question: 用户问题
            answer: 回答结果
            tenant_id: 租户ID
        """
        # TODO: 实现缓存写入
        raise NotImplementedError("CacheService.set_cache 尚未实现")
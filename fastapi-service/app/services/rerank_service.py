from typing import List

from app.core.constants import RERANK_TOP_N
from app.schemas.document import DocumentSchema


class RerankService:
    """重排序服务

    对向量检索的粗排结果进行精排，提升最终返回文档的准确性。
    """

    def rerank(
        self,
        query: str,
        documents: List[DocumentSchema],
        top_n: int = RERANK_TOP_N,
    ) -> List[DocumentSchema]:
        """对候选文档进行重排序

        TODO: 调用 BGE Reranker 模型（bge-reranker-large）对文档精排

        技术方案：
        - 使用 BGE Reranker（Cross-Encoder 架构）
        - 输入：query + 每个候选文档的 content，输出相关性分数
        - 按分数降序排列，取 Top-N 返回

        为什么需要重排序：
        - 向量检索（Bi-Encoder）：速度快，但 query 和 doc 独立编码，交互不充分
        - Reranker（Cross-Encoder）：速度慢，但 query 和 doc 联合编码，交互充分
        - Two-Stage：先用 Bi-Encoder 粗排（Top-K=10），再用 Cross-Encoder 精排（Top-N=5）
        - 面试讲：这是业界标准的「召回+排序」架构，类似搜索引擎的粗排→精排→重排流程，
          比单纯向量检索的准确率提升 10%-20%

        Args:
            query: 用户查询文本
            documents: 候选文档列表（向量检索粗排结果）
            top_n: 精排后保留的文档数量

        Returns:
            重排序后的文档列表，按相关性降序
        """
        # TODO: 实现重排序
        raise NotImplementedError("RerankService.rerank 尚未实现")
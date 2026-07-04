from typing import List

from app.core.constants import TOP_K
from app.schemas.document import DocumentSchema


class VectorService:
    """向量数据库服务

    封装向量存储和检索操作，支持多租户 Partition 隔离。
    """

    def add_documents(self, documents: List[DocumentSchema], tenant_id: str) -> None:
        """将文档向量存入向量数据库

        TODO: 将文档向量写入向量数据库（如 Milvus/FAISS），按 tenant_id 分区隔离

        技术方案：
        - 向量数据库选型：Milvus（分布式、高性能）或 FAISS（轻量级、单机）
        - 按 tenant_id 创建 Partition：每个租户的数据物理隔离，互不干扰
        - 面试讲：多租户数据隔离有三种方案：① 按 Collection 隔离（最彻底但管理复杂）
          ② 按 Partition 隔离（平衡性能和隔离性，推荐）③ 按字段过滤（简单但性能差）
          我们选择 Partition 方案，兼顾隔离性和查询效率

        Args:
            documents: 文档列表（含向量和元数据）
            tenant_id: 租户ID
        """
        # TODO: 实现向量入库
        raise NotImplementedError("VectorService.add_documents 尚未实现")

    def search(
        self, query_vector: List[float], tenant_id: str, top_k: int = TOP_K
    ) -> List[DocumentSchema]:
        """向量相似度检索

        TODO: 在指定租户 Partition 内检索 Top-K 最相似文档

        技术方案：
        - 使用余弦相似度（Cosine Similarity）或内积（IP）计算向量距离
        - 只在 tenant_id 对应的 Partition 中搜索，避免跨租户数据泄露
        - 面试讲：向量检索要做「多租户隔离 + 相似度过滤」，既要保证数据安全，
          又要过滤低质量结果（相似度 < 0.7 的通常不返回）

        Args:
            query_vector: 查询向量
            tenant_id: 租户ID
            top_k: 返回结果数量

        Returns:
            相似文档列表，按相似度降序排列
        """
        # TODO: 实现向量检索
        raise NotImplementedError("VectorService.search 尚未实现")

    def delete_by_document_id(self, document_id: str, tenant_id: str) -> None:
        """按文档ID删除向量

        TODO: 删除指定租户下指定文档的所有向量数据

        Args:
            document_id: 文档ID
            tenant_id: 租户ID
        """
        # TODO: 实现向量删除
        raise NotImplementedError("VectorService.delete_by_document_id 尚未实现")
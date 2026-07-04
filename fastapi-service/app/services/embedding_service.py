from typing import List


class EmbeddingService:
    """文本嵌入服务

    将文本转换为向量表示，用于语义搜索和相似度计算。
    """

    def embed(self, text: str) -> List[float]:
        """将单条文本转为向量

        TODO: 调用 BGE Embedding 模型（bge-large-zh-v1.5）将文本转为向量

        技术方案：
        - 使用 HuggingFace Transformers 或 ONNX Runtime 加载 BGE 模型
        - 模型选择：BAAI/bge-large-zh-v1.5（中文语义理解 SOTA 级别）
        - 向量维度：768（与 core/constants.py 中 EMBEDDING_DIMENSION 一致）
        - 面试讲：BGE 是 BAAI 开源的 Embedding 模型，在 MTEB 中文榜单排名领先，
          选择它的原因：开源免费、中文效果好、支持本地部署

        Args:
            text: 待嵌入的文本

        Returns:
            768 维浮点数向量
        """
        # TODO: 实现文本嵌入
        raise NotImplementedError("EmbeddingService.embed 尚未实现")

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """批量文本转向量

        TODO: 批量调用 BGE 模型，提升吞吐量

        技术方案：
        - 使用 model.encode(texts, batch_size=32) 批量处理
        - 批量处理比逐条调用效率高 5-10 倍
        - 面试讲：批量推理是生产环境必须考虑的优化手段，GPU 利用率直接影响成本

        Args:
            texts: 待嵌入的文本列表

        Returns:
            向量列表，每个向量为 768 维
        """
        # TODO: 实现批量嵌入
        raise NotImplementedError("EmbeddingService.embed_batch 尚未实现")
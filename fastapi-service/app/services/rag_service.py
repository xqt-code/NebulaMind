from typing import List, Optional

from app.models.request import AskRequest
from app.models.response import AskResponse

import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatTongyi
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage, SystemMessage


class RagService:
    """RAG（检索增强生成）服务

    协调整个 RAG 流程：缓存查询 → 向量检索 → 重排序 → Prompt 构建 → LLM 调用 → 结果缓存。
    """
    def __init__(self):
        self.embeddings = None
        # 初始化BGE Embedding模型
        # self.embeddings = HuggingFaceEmbeddings(
        #     model_name="BAAI/bge-small-zh-v1.5",
        #     model_kwargs={'device': 'cpu'},
        #     encode_kwargs={'normalize_embeddings': True}
        # )

        # 初始化通义千问
        self.llm = None
        # self.llm = ChatTongyi(
        #     model="qwen-plus",
        #     dashscope_api_key=settings.dashscope_api_key,
        #     streaming=True
        # )

        # 初始化向量库（先空，后续加载已有向量）
        self.vector_store = None

    def ask(self, request: AskRequest) -> AskResponse:
        """RAG 全流程入口

        TODO: 实现完整的 RAG（检索增强生成）流程，分步说明如下：

        1. 【缓存查询】调用 cache_service.get_similar_question() 检查语义缓存
           - 技术：Redis 语义缓存，通过相似度匹配历史问题
           - 价值：命中缓存直接返回，避免重复调用 LLM，大幅降低成本和延迟
           - 面试讲：Redis 语义缓存是 RAG 系统降本增效的关键手段，命中率可达 30%-50%

        2. 【向量检索】调用 embedding_service.embed() 将问题转为向量，
           再调用 vector_service.search() 检索 Top-K 相关文档片段
           - 技术：BGE Embedding 模型 + 向量数据库（如 Milvus/FAISS）
           - 为什么用 BGE：中文语义理解业界领先，MTEB 榜单排名靠前
           - 面试讲：向量检索是 RAG 的核心，决定了「召回」质量，Top-K 和相似度阈值是调优重点

        3. 【重排序】调用 rerank_service.rerank() 对候选文档精排
           - 技术：BGE Reranker 模型（Cross-Encoder 架构）
           - 为什么需要重排序：向量检索（Bi-Encoder）速度快但精度一般，Rerank（Cross-Encoder）精度高但速度慢，
             两者结合是业界标准做法：粗排（Bi-Encoder）+ 精排（Cross-Encoder）
           - 面试讲：Two-Stage 检索是 RAG 的标配，能显著提升答案质量

        4. 【Prompt 构建】将用户问题 + 重排序后的文档片段 + 系统提示词组装成完整 Prompt
           - 技术：Prompt Engineering，包含角色设定、上下文注入、输出格式约束
           - 面试讲：好的 Prompt 设计能让大模型输出更准确，常用技巧包括 Few-Shot、Chain-of-Thought

        5. 【LLM 调用】调用 llm_service.chat() 获取大模型回答
           - 技术：通义千问 API，支持 JSON Mode 结构化输出
           - 面试讲：选择国内大模型（通义千问）而非 OpenAI，考虑数据合规和成本因素

        6. 【结果缓存】调用 cache_service.set_cache() 将问答对存入缓存
           - 为后续相似问题提供快速命中

        7. 返回 AskResponse 对象
        """
        # TODO: 实现上述流程
        raise NotImplementedError("RagService.ask 尚未实现")
from typing import List, Optional

from app.models.request import AskRequest
from app.models.response import AskResponse

# typing: 类型注解，告诉调用方这个方法返回什么类型
from typing import Dict, Any, List, Optional

# logger: 打印日志，方便调试和追踪问题
from app.utils.logger import get_logger

# ResponseBuilder: 统一响应构建器（把结果包装成统一格式返回给前端）
from app.core.response_builder import ResponseBuilder

# LLMRepository: 数据层，负责调用通义千问 API
from app.repositories.llm_repository import LLMRepository

# 导入 LangChain 的向量库和向量化组件
# （这些是 LangChain 提供的工具，不需要我们重新实现）
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

import os  # 用于检查文件/目录是否存在

# 创建日志记录器，用于打印此模块的信息
logger = get_logger(__name__)


class RagService:
    """
        企业级 RAG 服务

        完整流程：
        1. 缓存查询（Redis 语义缓存）
        2. 向量检索（BGE Embedding + FAISS）
        3. 重排序（BGE Reranker）
        4. Prompt 构建（System + 上下文 + 用户问题）
        5. LLM 调用（通义千问）
        6. 结果缓存（存入 Redis）

    特点：
        - 每一步都有日志，方便调试和监控
        - 降级策略：任何一步失败都优雅降级
        - 缓存机制：降低成本和延迟
        - 引用溯源：返回文档片段和相似度
    """

    # 类常量：便于统一修改
    VECTOR_STORE_PATH = "./data/vector_store"  # 向量库路径
    CACHE_EXPIRE_SECONDS = 3600 * 24 * 7  # 缓存过期时间（7天）
    SIMILARITY_THRESHOLD = 0.3  # 相似度阈值（低于此值视为不相关）
    TOP_K_RETRIEVE = 10  # 初次检索返回数量
    TOP_K_RERANK = 3  # 重排序后最终使用的数量

    def __init__(self):
        """
            初始化 RAG 服务

            做什么：
            - 初始化大模型数据仓库
            - 加载向量库（如果存在）
            - 初始化重排序器（如果可用）
            - 初始化 Redis 缓存（如果可用）

            协调整个 RAG 流程：缓存查询 → 向量检索 → 重排序 → Prompt 构建 → LLM 调用 → 结果缓存。
        """

        # ---- 第 1 步：创建大模型调用层 ----
        # LLMRepository 负责调用通义千问 API
        # 它不需要关心检索逻辑，只负责"给一段文本，返回大模型的回答"

        self.llm_repo = LLMRepository()
        logger.info("LLM数据仓库初始化完成")

        # ---- 第 2 步：初始化向量库为 None ----
        # self.vector_store 初始为 None，表示"尚未加载成功"
        # 后面可以通过判断 self.vector_store is None 来决定是否走 RAG 流程
        self.vector_store = None
        self.retriever = None  # 基础件所起(无重排序)
        self.reranker = None   # 重排序器
        self.compression_retriever = None # 带重排序的检索器

        # ---- 第 3 步：尝试加载向量库 ----
        # 如果向量库文件存在，就加载；否则跳过，使用纯对话模式
        vector_store_path = "./data/vector_store"  # 向量库保存的目录

        # 检查目录是否存在（如果不存在，说明还没有导入任何文档）
        if not os.path.exists(vector_store_path):
            logger.warning(f"向量库目录不存在: {vector_store_path}，将使用纯对话模式")
            return

        # 检查目录里是否有 FAISS 索引文件（index.faiss 和 index.pkl）
        if not os.path.exists(os.path.join(vector_store_path, "index.faiss")):
            logger.warning(f"向量库索引文件不存在: {vector_store_path}/index.faiss，将使用纯对话模式")
            return

        try:
            # ---- 第 4 步：加载向量化模型 ----
            # 这里的模型必须和 import_docs.py 里用的向量化模型完全一致
            # 因为向量库里的向量就是用这个模型生成的，只有用同一个模型才能正确匹配
            embeddings = HuggingFaceEmbeddings(
                model_name = "BAAI/bye-small-zh-v1.5",  #中文语义模型
                model_kwargs = {"device": "cpu"},       # 用CPU推理(速度足够)
                encode_kwargs = {"normalize_embeddings": True},  # 归一化向量,提高检索精度
            )

            # ---- 第 5 步：加载 FAISS 向量库 ----
            # FAISS.load_local 会读取本地文件，重建索引
            # allow_dangerous_deserialization=True 是 LangChain 1.0 后的安全要求，加载本地索引必须显式声明
            self.vector_store = FAISS.load_local(
                vector_store_path,
                embeddings,
                allow_dangerous_deserialization=True,  # 明确告知“我知道这是本地文件，允许加载”
            )

            # 打印加载成功的日志，并显示向量数量
            logger.info(f"向量库加载成功，包含 {self.vector_store.index.ntotal} 个向量")
        except Exception as e:
            # 如果加载过程中出现任何异常（比如文件损坏、版本不匹配等），记录错误并保持纯对话模式
            logger.error(f"加载向量库失败: {e}，将使用纯对话模式")
            self.vetor_store = None  # 确保 vector_store 是 None

    # =========================================================================
    # ask 方法 —— RAG 问答的核心入口
    # =========================================================================
    def ask(self, question: str, tenant_id: str = "1") -> Dict[str, Any]:
        """
        RAG 问答入口

        参数:
            question: 用户问题
            tenant_id: 租户 ID（多租户场景用，目前固定为 "1"）

        返回:
            统一格式的字典，包含：
                - answer: AI 回答
                - references: 引用列表（文件名、片段、相似度）
                - confidence: 置信度（目前固定为 0.8）
                - has_answer: 是否有效回答

        完整执行流程:
            1. 检查向量库是否可用
            2. 用用户问题执行向量检索（找最相关的 Top 5 文档片段）
            3. 提取检索结果，构建引用列表和上下文
            4. 把 System Prompt + 检索到的上下文 + 用户问题拼成完整 Prompt
            5. 调用大模型生成回答
            6. 返回回答 + 引用来源

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
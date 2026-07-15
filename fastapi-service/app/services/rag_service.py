import os
import json
import time  # 确保文件顶部已经导入 time
from typing import Dict, Any, List, Optional

# 日志
from app.utils.logger import get_logger

# 统一响应构建器
from app.core.response_builder import ResponseBuilder

# 数据层：大模型调用
from app.repositories.llm_repository import LLMRepository

# LangChain 向量化和向量库
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# LangChain 重排序器（Cross-Encoder）
# from langchain_community.document_compressors.cross_encoder_reranker import CrossEncoderReranker
# from langchain_community.cross_encoders import HuggingFaceCrossEncoder

# LangChain 检索器（将向量库包装成检索器接口）
from langchain.retrievers import ContextualCompressionRetriever

# Redis 缓存（如果需要）
import redis
from app.core.config import settings

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
    SIMILARITY_THRESHOLD = 0.6  # 相似度阈值（低于此值视为不相关）
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
        self._load_vector_store()
        # vector_store_path = "./data/vector_store"  # 向量库保存的目录

        # ---- 4. 初始化重排序器（如果向量库加载成功） ----
        # if self.vector_store is not None:
        #     self._init_reranker()

        # ---- 5. 初始化 Redis 缓存（如果可用） ----
        self.redis_client = None
        self._init_redis()

        logger.info("RagService 初始化完成")

    # =========================================================================
    # 初始化辅助方法（私有方法）
    # =========================================================================
    def _load_vector_store(self):
        """加载 FAISS 向量库（如果存在）"""
        if not os.path.exists(self.VECTOR_STORE_PATH):
            logger.warning(f"向量库目录不存在: {self.VECTOR_STORE_PATH}，将使用纯对话模式")
            return

        # 修复：用 os.path.join 组合路径
        index_path = os.path.join(self.VECTOR_STORE_PATH, "index.faiss")
        if not os.path.exists(index_path):
            logger.warning("向量库索引文件不存在，将使用纯对话模式")
            return

        try:
            # 使用相同的 Embedding 模型（必须和导入时一致）
            embeddings = HuggingFaceEmbeddings(
                model_name="BAAI/bge-small-zh-v1.5",
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True},
            )

            # 加载 FAISS 索引
            self.vector_store = FAISS.load_local(
                self.VECTOR_STORE_PATH,
                embeddings,
                allow_dangerous_deserialization=True
            )

            # 创建基础检索器（无重排序，用于召回）
            self.retriever = self.vector_store.as_retriever(
                search_kwargs={"k": self.TOP_K_RETRIEVE}
            )

            logger.info(f"向量库加载成功，包含 {self.vector_store.index.ntotal} 个向量")
        except Exception as e:
            logger.error(f"加载向量库失败: {e}，将使用纯对话模式")
            self.vector_store = None


    # def _init_reranker(self):
        """初始化重排序器（BGE Reranker）"""
        # try:
        #     # Cross-Encoder 模型（精排，精度高）
        #     # 注意：这里使用了 BAAI/bge-reranker-v2-m3，是一个轻量高效的模型
        #     reranker_model = HuggingFaceCrossEncoder(
        #         model_name="BAAI/bge-reranker-v2-m3",
        #         model_kwargs={"device": "cpu"},
        #     )
        #     self.reranker = CrossEncoderReranker(
        #         model=reranker_model,
        #         top_n=self.TOP_K_RERANK,
        #     )
        #
        #     # 创建带重排序的检索器（压缩检索器）
        #     self.compression_retriever = ContextualCompressionRetriever(
        #         base_compressor=self.reranker,
        #         base_retriever=self.retriever,
        #     )
        #
        #     logger.info("重排序器初始化成功")
        # except Exception as e:
        #     logger.warning(f"重排序器初始化失败: {e}，将使用基础向量检索（无重排序）")
        #     self.reranker = None
        #     self.compression_retriever = None

    def _init_redis(self):
        """初始化 Redis 缓存（如果配置了 Redis）"""
        try:
            # 从配置读取 Redis 连接信息（需要在 settings 中定义）
            if hasattr(settings, 'redis_host') and settings.redis_host:
                self.redis_client = redis.Redis(
                    host=settings.redis_host,
                    port=settings.redis_port,
                    db=settings.redis_db,
                    decode_responses=True,
                    socket_connect_timeout=2,
                    socket_timeout=2,
                )
                # 测试连接
                self.redis_client.ping()
                logger.info("Redis 缓存连接成功")
            else:
                logger.info("Redis 未配置，缓存功能禁用")
        except Exception as e:
            logger.warning(f"Redis 连接失败: {e}，缓存功能禁用")
            self.redis_client = None

    # =========================================================================
    # ask 方法 —— RAG 问答的核心入口
    # =========================================================================
    def ask(self, question: str, tenant_id: str = "1") -> Dict[str, Any]:
        """
        RAG 问答入口（完整六步流程）

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
        # raise NotImplementedError("RagService.ask 尚未实现")
        logger.info(f"RAG 问答开始: question={question[:30]}..., tenant={tenant_id}")

        # ---- 第1步：缓存查询（语义缓存） ----
        # 检查是否有历史相似问题的缓存答案
        cached = self._get_cache(question, tenant_id)
        if cached:
            logger.info("命中缓存，直接返回")
            return cached

        # ---- 准备 System Prompt（始终需要） ----
        system_prompt = """
        你是 NebulaMind 企业内部智能助手。

        【核心规则】
        1. 只能基于下面提供的【参考文档】回答用户的问题。
        2. 如果参考文档中没有相关内容，必须回答："抱歉，知识库中没有找到相关内容，请联系管理员补充。"
        3. 绝对不允许编造答案，不允许回答和知识库无关的问题。
        4. 回答要简洁、准确、专业，使用中文。
        5. 必须严格按照指定的 JSON 格式返回结果。
        """

        try:
            # ---- 第2步：向量检索（召回） ----
            # 如果向量库未加载，降级为纯对话
            if self.vector_store is None:
                logger.warning("向量库未加载，降级为纯对话模式")
                fallback_answer = self.llm_repo.chat(
                    prompt=question,
                    system_prompt=system_prompt
                )
                return ResponseBuilder.fallback(fallback_answer, reason="向量库未加载")

            # 使用检索器获取文档片段
            # 如果有重排序检索器，用压缩检索器；否则用基础检索器
            # if self.compression_retriever is not None:
            #     # 带重排序的检索（精排）
            #     docs = self.compression_retriever.get_relevant_documents(question)
            #     logger.info(f"重排序检索完成，返回 {len(docs)} 个文档")

            # 基础向量检索（无重排序）
            docs_with_scores = self.vector_store.similarity_search_with_score(
                question,
                k=self.TOP_K_RETRIEVE
            )
            # 过滤低相似度结果
            docs_with_scores = [(doc, score) for doc, score in docs_with_scores if
                                score > self.SIMILARITY_THRESHOLD]
            docs = [doc for doc, _ in docs_with_scores[:self.TOP_K_RERANK]]
            logger.info(f"基础检索完成，过滤后 {len(docs)} 个文档")

            # 如果检索结果为空，降级
            if not docs:
                logger.warning("检索无结果，降级为纯对话模式")
                fallback_answer = self.llm_repo.chat(
                    prompt=question,
                    system_prompt=system_prompt
                )
                return ResponseBuilder.fallback(fallback_answer, reason="检索无结果")

            # ---- 第3步：构建引用列表和上下文 ----
            references = []
            context_parts = []

            for doc, score in docs_with_scores[:self.TOP_K_RERANK]:  # 注意这里遍历的是元组
                # 提取文件名
                source = doc.metadata.get("source", "未知文档")
                if "\\" in source:
                    source = source.split("\\")[-1]
                if "/" in source:
                    source = source.split("/")[-1]

                # 构建引用信息（把 score 传进去）
                references.append({
                    "file_name": source,
                    "content": doc.page_content[:200] + ("..." if len(doc.page_content) > 200 else ""),
                    "similarity": float(score),  # <--- 现在取到真实分数了
                })
                context_parts.append(doc.page_content)

            context = "\n\n---\n\n".join(context_parts)

            # ---- 第4步：Prompt 构建 ----
            full_prompt = f"""{system_prompt}

        【参考文档】
        {context}

        【用户问题】
        {question}

        请基于上述参考文档回答用户的问题。如果参考文档中没有相关内容，请明确告知。"""

            # ---- 第5步：LLM 调用 ----
            start_time = time.time()  # 记录开始时间
            llm_result = self.llm_repo.chat(
                prompt=full_prompt,
                system_prompt=None
            )
            elapsed_ms = int((time.time() - start_time) * 1000)  # 计算毫秒

            answer = llm_result["content"]  # 提取回答内容
            token_usage = {  # 组装 Token 数据
                "prompt_tokens": llm_result["prompt_tokens"],
                "completion_tokens": llm_result["completion_tokens"],
                "total_tokens": llm_result["total_tokens"]
            }

            logger.info(
                f"RAG 问答完成，耗时 {elapsed_ms}ms，回答长度: {len(answer)} 字符，召回 {len(references)} 个文档片段")

            logger.info(f"RAG 问答完成，回答长度: {len(answer)} 字符，召回 {len(references)} 个文档片段")

            # ---- 第5.5步：计算动态置信度（平滑映射算法） ----
            if not references:
                dynamic_confidence = 0.1
            else:
                avg_score = sum(ref["similarity"] for ref in references) / len(references)

                # 假设 BGE 分数大多落在 0.3 ~ 0.9 之间
                # 低于 0.3 视为极低相关，高于 0.9 视为完美匹配
                min_score, max_score = 0.3, 0.9
                min_conf, max_conf = 0.15, 0.95

                # 把 avg_score 从 [0.3, 0.9] 区间线性映射到 [0.15, 0.95]
                if avg_score <= min_score:
                    dynamic_confidence = min_conf
                elif avg_score >= max_score:
                    dynamic_confidence = max_conf
                else:
                    # 线性插值公式
                    dynamic_confidence = min_conf + (avg_score - min_score) / (max_score - min_score) * (
                                max_conf - min_conf)

                # 保留两位小数，更好看
                dynamic_confidence = round(dynamic_confidence, 2)

            # ---- 第6步：结果缓存 ----
            # 构建响应数据

            response_data = ResponseBuilder.success(
                answer=answer,
                references=references,
                confidence=dynamic_confidence,
                latency_ms=elapsed_ms,  # 🔥 新增：耗时
                token_usage=token_usage  # 🔥 新增：Token 消耗
            )

            # 异步存入缓存（不阻塞主流程）
            self._set_cache(question, tenant_id, response_data)

            return response_data

        except Exception as e:
            logger.error(f"RAG 问答失败: {e}")
            return ResponseBuilder.error(str(e))

        # =========================================================================
        # 缓存辅助方法（私有方法）
        # =========================================================================

    def _get_cache(self, question: str, tenant_id: str) -> Optional[Dict[str, Any]]:
        """
        从 Redis 获取缓存（语义缓存）

        注意：这是一个简化的语义缓存实现，真实场景可结合 Embedding 相似度
        这里我们直接用问题原文作为 key（精确匹配），适合高频重复问题。
        更高级的语义缓存需要计算问题向量的相似度。
        """
        if self.redis_client is None:
            return None

        # 用 tenant_id + 问题哈希作为 key
        cache_key = f"rag:cache:{tenant_id}:{hash(question)}"
        try:
            cached_json = self.redis_client.get(cache_key)
            if cached_json:
                return json.loads(cached_json)
        except Exception as e:
            logger.warning(f"读取缓存失败: {e}")
        return None

    def _set_cache(self, question: str, tenant_id: str, response_data: Dict[str, Any]):
        """存入缓存（非阻塞，失败不影响主流程）"""
        if self.redis_client is None:
            return

        cache_key = f"rag:cache:{tenant_id}:{hash(question)}"
        try:
            self.redis_client.setex(
                cache_key,
                self.CACHE_EXPIRE_SECONDS,
                json.dumps(response_data, ensure_ascii=False)
            )
            logger.info("缓存写入成功")
        except Exception as e:
            logger.warning(f"缓存写入失败: {e}")


# HTTP 请求追踪 ID 的请求头字段名（与 Java 侧 Constants.TRACE_ID_HEADER 保持一致）
TRACE_ID_HEADER = "X-Trace-ID"

# 默认租户 ID，用于多租户场景下的默认租户标识
DEFAULT_TENANT_ID = "1"

# BGE 嵌入模型的向量维度（768 维）
EMBEDDING_DIMENSION = 768

# 向量检索默认返回的 Top-K 候选数量
TOP_K = 10

# Rerank 重排序后保留的 Top-N 结果数量
RERANK_TOP_N = 5
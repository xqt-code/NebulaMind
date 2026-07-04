from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置，使用 pydantic-settings 从 .env.dev 加载环境变量"""

    # 应用名称
    app_name: str = "NebulaMind-AI-Service"

    # 运行环境标识（dev/test/prod）
    env: str = "dev"

    # 调试模式，开发环境开启
    debug: bool = False

    # 服务监听地址
    host: str = "0.0.0.0"

    # 服务监听端口
    port: int = 8000

    # 阿里云 DashScope API Key（预留，用于 LLM 调用）
    dashscope_api_key: str = ""

    # 大语言模型名称（预留，默认使用通义千问 Plus）
    llm_model: str = "qwen-plus"

    # 向量存储路径（预留，用于本地向量数据库持久化）
    vector_store_path: str = "./data/vector_store"

    # Redis 主机地址（预留，用于缓存与消息队列）
    redis_host: str = "localhost"

    # Redis 端口（预留）
    redis_port: int = 6379

    # Redis 密码（预留）
    redis_password: str = ""

    # Redis 数据库编号（预留）
    redis_db: int = 0

    class Config:
        env_file = ".env.dev"
        env_file_encoding = "utf-8"


settings = Settings()
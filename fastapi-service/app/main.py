"""
NebulaMind AI 推理服务 - 应用入口文件（main.py）

【职责】
本文件是整个 FastAPI 应用的“启动装配工厂”，只负责：
1. 创建 FastAPI 实例（app）
2. 注册全局中间件（CORS、TraceID）
3. 注册全局异常处理器
4. 挂载路由（API 接口）

【不做什么】
- 不写任何业务逻辑（RAG、向量检索等）
- 不直接处理数据库连接
- 不定义数据模型（DTO）
"""

# =============================================================================
# 1. 导入依赖模块
# =============================================================================
# FastAPI 核心类
from fastapi import FastAPI
# FastAPI 内置的 CORS 中间件（处理跨域请求）
from fastapi.middleware.cors import CORSMiddleware

# 导入项目自定义模块
# 注意：这些模块的路径基于项目根目录，Python 会根据 sys.path 查找
from app.api.v1.router import router as v1_router          # 所有 v1 版本 API 路由的总入口
from app.core.config import settings                       # 统一配置管理（从 .env 读取）
from app.core.exceptions import register_exception_handlers  # 全局异常处理器注册函数
from app.core.response import ResponseModel                # 统一响应格式
from app.middlewares.trace_id_middleware import TraceIDMiddleware  # TraceID 中间件类
from app.utils.logger import get_logger                    # 获取统一日志记录器

# =============================================================================
# 2. 初始化日志
# =============================================================================
# __name__ 是当前模块名（app.main），日志中会显示这个名称，便于排查问题
# 为什么显式初始化？Python 没有编译期注解，必须显式创建 logger 实例
# 这等同于 Java 中 @Slf4j 注解在编译期生成的代码
logger = get_logger(__name__)


# =============================================================================
# 3. 创建 FastAPI 应用实例（核心）
# =============================================================================
# app 是整个应用的根对象，所有的路由、中间件都挂在它上面
# 这些元数据会出现在自动生成的 API 文档（/docs）中
app = FastAPI(
    title="NebulaMind AI 推理服务",                         # 文档标题
    description="企业级智能知识库系统 - AI 推理核心服务",        # 文档描述
    version="1.0.0",                                      # API 版本号
    docs_url="/docs",                                     # Swagger UI 文档路径（默认就是 /docs）
    redoc_url="/redoc",                                   # ReDoc 文档路径（可选）
)


# =============================================================================
# 4. 注册中间件（按执行顺序）
# =============================================================================
# 【重要】中间件的注册顺序决定了执行顺序：
# 1. CORS 必须最先注册，因为跨域请求需要最先被处理
# 2. TraceID 紧随其后，确保后续所有日志都携带 TraceID
# 3. 其他中间件（如限流、鉴权）按需添加

# 4.1 CORS 中间件（跨域资源共享）
# 为什么需要？前端 Vue 项目（运行在 5173 端口）要访问本服务（8000 端口），
# 跨域是浏览器安全策略，必须由后端明确放行。
# 生产环境建议 allow_origins 限制为具体的前端域名，不要用 "*"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # 允许所有来源（开发环境方便）
    allow_credentials=True,        # 允许携带 cookie
    allow_methods=["*"],           # 允许所有 HTTP 方法（GET、POST、PUT、DELETE 等）
    allow_headers=["*"],           # 允许所有请求头
)

# 4.2 TraceID 中间件（全链路追踪）
# 作用：为每一个请求生成或提取 TraceID，并存入日志上下文。
# 这样，分散在不同服务（Java、Python）的日志可以通过同一个 TraceID 串联起来。
# 必须注册在 CORS 之后，确保响应头也能携带 TraceID。
app.add_middleware(TraceIDMiddleware)

# 【备选】如果后续需要其他中间件（如限流、鉴权），按顺序添加在此处：
# app.add_middleware(RateLimitMiddleware)   # 限流中间件
# app.add_middleware(AuthMiddleware)        # 鉴权中间件


# =============================================================================
# 5. 注册全局异常处理器
# =============================================================================
# 作用：捕获所有路由中抛出的未被捕获的异常，统一转换为标准的 ResponseModel 格式。
# 例如：如果业务代码抛出自定义 BusinessException，这里会拦截并返回：
# {"code": 500, "msg": "知识库未找到", "data": null}
# 这样可以保证所有异常响应格式一致，前端只需处理一种格式。
register_exception_handlers(app)


# =============================================================================
# 6. 注册路由（API 接口）
# =============================================================================
# 6.1 注册 v1 版本的所有路由（推荐使用统一聚合器）
# v1_router 已经包含了 health、chat、document 等所有子路由，
# 通过 include_router 一次性挂载到 app 上。
app.include_router(v1_router)

# 【说明】如果你没有使用统一的 v1_router，也可以逐个注册子路由，例如：
# app.include_router(health.router, prefix="/api/v1", tags=["系统管理"])
# app.include_router(chat.router, prefix="/api/v1", tags=["智能问答"])
# 但使用 v1_router 更清晰，便于维护。

# 6.2 根路径（可选）
# 作用：访问根路径返回服务基本信息，方便快速确认服务是否存活。
# 这个路径不是必须的，但可以保留作为最简单的健康检查。
@app.get("/")
async def root():
    """根路径，返回服务基本信息（用于简单存活检测）"""
    logger.info("根路径被访问")
    return ResponseModel.success(
        data={
            "service": "NebulaMind AI 推理服务",
            "version": "1.0.0",
            "status": "running"
        }
    )


# =============================================================================
# 7. 启动日志（输出服务启动信息）
# =============================================================================
# 在服务启动后打印关键配置信息，方便运维人员确认环境。
logger.info(
    f"服务启动完成 | "
    f"应用: {settings.app_name} | "
    f"环境: {settings.env} | "
    f"监听: {settings.host}:{settings.port}"
)

# =============================================================================
# 【补充说明】
# 为什么没有 main() 函数？
# FastAPI 应用通过 uvicorn 命令直接启动：uvicorn app.main:app --reload
# uvicorn 会直接读取 app 变量，所以不需要 if __name__ == "__main__" 包裹。
# 如果你希望直接运行此文件（python main.py），可以添加以下代码：
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
# 但企业级部署通常用 uvicorn 命令行启动，因此一般不写这部分。
# =============================================================================


@app.get("/health")
async def health_check():
    return {"status": "ok"}

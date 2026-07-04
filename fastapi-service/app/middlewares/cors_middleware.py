from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app) -> None:
    """配置 CORS 跨域中间件

    开发环境允许所有源、所有方法、所有头，生产环境可按需配置 allow_origins 列表。
    """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 生产环境应替换为具体域名列表
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
# NebulaMind AI 推理服务

企业级智能知识库系统 - AI 推理核心服务，提供基于 FastAPI 的高性能 RESTful API。

## 技术栈

- **Web 框架**: FastAPI 0.115.6
- **ASGI 服务器**: Uvicorn 0.34.0
- **数据验证**: Pydantic 2.10.4
- **配置管理**: pydantic-settings 2.6.1 + python-dotenv 1.0.1
- **Python 版本**: 3.10+

## 快速启动

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动开发服务器
python -m uvicorn app.main:app --reload

# 3. 访问服务
#    API 根路径: http://localhost:8000/
#    Swagger 文档: http://localhost:8000/docs
```

## 项目结构

```
fastapi-service/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用入口
│   └── core/
│       ├── __init__.py
│       ├── config.py         # 配置管理
│       ├── constants.py      # 常量定义
│       ├── response.py       # 统一响应模型
│       └── enums.py          # 错误码枚举
├── .env.dev                  # 开发环境配置
├── .env.test                 # 测试环境配置
├── .env.prod                 # 生产环境配置
├── requirements.txt          # 依赖清单
└── README.md
```
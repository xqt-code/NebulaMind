from fastapi import APIRouter

from app.api.v1.routes import chat, document, health

router = APIRouter(prefix="/api/v1")

# 聚合所有子路由
router.include_router(health.router)
router.include_router(document.router)
router.include_router(chat.router)
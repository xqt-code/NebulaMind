from fastapi import APIRouter

from app.core.response import ResponseModel

router = APIRouter(tags=["系统管理"])


@router.get("/health")
async def health_check():
    """服务健康检查"""
    return ResponseModel.success(
        data={"status": "ok", "service": "nebulamind-ai-service"}
    )
from fastapi import APIRouter

from app.core.response import ResponseModel
from app.models.request import DocumentProcessRequest

router = APIRouter(prefix="/documents", tags=["文档管理"])


@router.post("/upload")
async def upload_document(request: DocumentProcessRequest):
    """上传并处理文档

    TODO: 调用 rag_service.process_document() 实现文档上传和向量化入库

    流程说明：
    1. 接收文档内容，调用 text_splitter 进行文本切片
    2. 调用 embedding_service.embed_batch() 批量生成向量
    3. 调用 vector_service.add_documents() 存入向量数据库
    4. 返回任务ID和状态

    面试讲：文档处理是 RAG 系统的「数据预处理」环节，需要关注：
    - 文本切片策略（chunk_size 和 overlap 的平衡）
    - 向量化效率（批量处理 vs 逐条处理）
    - 异步处理（大文档用 Celery 等任务队列异步处理）
    """
    # TODO: 实现文档处理流程
    return ResponseModel.success(
        data={
            "task_id": "TODO",
            "status": "pending",
            "message": "文档处理功能待实现",
        }
    )


@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """删除文档向量

    TODO: 调用 vector_service.delete_by_document_id() 删除文档的所有向量数据

    面试讲：删除操作需要确保数据一致性：
    - 向量库和原始文档存储要同步删除
    - 考虑软删除（标记删除）+ 定期清理的策略
    """
    # TODO: 实现文档删除
    return ResponseModel.success(
        data={"message": f"文档 {document_id} 删除功能待实现"}
    )
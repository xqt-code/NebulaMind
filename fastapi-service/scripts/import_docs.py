"""
批量导入文档到向量库（FAISS）
使用方法：python scripts/import_docs.py --dir ./test_docs
"""

import os
import sys
import argparse
from pathlib import Path

# 添加项目根目录到 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_community.document_loaders import TextLoader, PyPDFLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

# 支持的文档类型
LOADER_MAP = {
    ".txt": TextLoader,
    ".md": UnstructuredMarkdownLoader,
    ".pdf": PyPDFLoader,
}


def load_documents(file_path: str):
    """根据文件扩展名加载文档"""
    ext = Path(file_path).suffix.lower()
    loader_cls = LOADER_MAP.get(ext)
    if loader_cls is None:
        logger.warning(f"跳过不支持的文件类型: {file_path}")
        return None
    try:
        # 对 txt 文件指定 GBK 编码（如果 UTF-8 读取失败则自动尝试 GBK）
        if ext == ".txt":
            loader = loader_cls(file_path, encoding="utf-8", autodetect_encoding=True)
        else:
            loader = loader_cls(file_path)
        # 读取源文件 → 解析内容 → 包装成 LangChain 的 Document 对象列表 → 返回给调用方。
        docs = loader.load()
        logger.info(f"加载成功: {file_path}，共 {len(docs)} 页/段")
        return docs
    except Exception as e:
        logger.error(f"加载失败 {file_path}: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="批量导入文档到向量库")
    parser.add_argument("--dir", required=True, help="文档目录路径")
    parser.add_argument("--chunk_size", type=int, default=500, help="切片大小")
    parser.add_argument("--chunk_overlap", type=int, default=50, help="切片重叠字符数")
    parser.add_argument("--output", default="./data/vector_store", help="向量库保存路径")
    args = parser.parse_args()

    doc_dir = Path(args.dir)
    if not doc_dir.exists():
        logger.error(f"目录不存在: {doc_dir}")
        return

    # 收集所有文档
    all_docs = []
    for ext in LOADER_MAP.keys():
        for file_path in doc_dir.glob(f"*{ext}"):
            docs = load_documents(str(file_path))
            if docs:
                all_docs.extend(docs)

    if not all_docs:
        logger.warning("未找到任何可导入的文档")
        return

    logger.info(f"共加载 {len(all_docs)} 个文档片段")

    # 切片
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""],
    )
    chunks = text_splitter.split_documents(all_docs)
    logger.info(f"切片后共 {len(chunks)} 个 chunk")

    # 向量化并存入 FAISS
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-zh-v1.5",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local(args.output)
    logger.info(f"向量库已保存到: {args.output}，共 {vector_store.index.ntotal} 个向量")


if __name__ == "__main__":
    main()
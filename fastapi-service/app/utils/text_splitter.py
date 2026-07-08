from typing import List


class TextSplitter:
    """文本切片工具（预留）

    用于将长文本按指定大小切分为重叠的片段，供向量化入库使用。
    """

    def split_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """将文本切分为多个片段

        Args:
            text: 待切分的原始文本
            chunk_size: 每个片段的最大字符数
            overlap: 相邻片段之间的重叠字符数

        Returns:
            切分后的文本片段列表
        """
        # TODO: 实现具体的文本切片逻辑（按字符/语义边界切分，支持重叠）
        raise NotImplementedError("TextSplitter.split_text 尚未实现")
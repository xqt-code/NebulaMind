package com.nebulamind.kb.dao.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.nebulamind.kb.common.result.PageResult;
import com.nebulamind.kb.dao.entity.Document;
import org.apache.ibatis.annotations.Mapper;

/**
 * 文档 Mapper 接口。
 * 继承 MyBatis-Plus BaseMapper，提供对 biz_document 表的 CRUD 操作。
 *
 * @author NebulaMind
 */
@Mapper
public interface DocumentMapper extends BaseMapper<Document> {
}
package com.nebulamind.kb.dao.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.nebulamind.kb.dao.entity.Message;
import org.apache.ibatis.annotations.Mapper;

/**
 * 消息 Mapper 接口。
 * 继承 MyBatis-Plus BaseMapper，提供对 biz_message 表的 CRUD 操作。
 *
 * @author NebulaMind
 */
@Mapper
public interface MessageMapper extends BaseMapper<Message> {
}
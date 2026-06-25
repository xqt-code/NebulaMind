package com.nebulamind.kb.dao.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.nebulamind.kb.dao.entity.Conversation;
import org.apache.ibatis.annotations.Mapper;

/**
 * 会话 Mapper 接口。
 * 继承 MyBatis-Plus BaseMapper，提供对 biz_conversation 表的 CRUD 操作。
 *
 * @author NebulaMind
 */
@Mapper
public interface ConversationMapper extends BaseMapper<Conversation> {
}
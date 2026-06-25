package com.nebulamind.kb.dao.entity;

import com.baomidou.mybatisplus.annotation.TableName;
import com.nebulamind.kb.common.entity.BaseEntity;

/**
 * 消息实体类。
 * 对应数据库表 biz_message，用于存储会话中的每一条消息记录。
 *
 * @author NebulaMind
 */
@TableName("biz_message")
public class Message extends BaseEntity {
}
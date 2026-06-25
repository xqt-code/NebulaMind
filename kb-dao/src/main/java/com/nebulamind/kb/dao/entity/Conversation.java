package com.nebulamind.kb.dao.entity;

import com.baomidou.mybatisplus.annotation.TableName;
import com.nebulamind.kb.common.entity.BaseEntity;

/**
 * 会话实体类。
 * 对应数据库表 biz_conversation，用于存储用户与 AI 的对话会话信息。
 *
 * @author NebulaMind
 */
@TableName("biz_conversation")
public class Conversation extends BaseEntity {
}
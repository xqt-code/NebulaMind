package com.nebulamind.kb.dao.entity;

import com.baomidou.mybatisplus.annotation.TableName;
import com.nebulamind.kb.common.entity.BaseEntity;

/**
 * 任务实体类。
 * 对应数据库表 sys_task，用于存储系统异步任务信息。
 *
 * @author NebulaMind
 */
@TableName("sys_task")
public class Task extends BaseEntity {
}
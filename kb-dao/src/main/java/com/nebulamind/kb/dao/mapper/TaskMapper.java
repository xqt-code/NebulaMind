package com.nebulamind.kb.dao.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.nebulamind.kb.dao.entity.Task;
import org.apache.ibatis.annotations.Mapper;

/**
 * 任务 Mapper 接口。
 * 继承 MyBatis-Plus BaseMapper，提供对 sys_task 表的 CRUD 操作。
 *
 * @author NebulaMind
 */
@Mapper
public interface TaskMapper extends BaseMapper<Task> {
}
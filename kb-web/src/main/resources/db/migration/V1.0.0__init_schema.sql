-- 初始化 NebulaMind 数据库表结构

-- 文档表
CREATE TABLE IF NOT EXISTS `biz_document` (
    `id` BIGINT NOT NULL COMMENT '文档ID',
    `tenant_id` BIGINT NOT NULL COMMENT '租户ID',
    `file_name` VARCHAR(255) NOT NULL COMMENT '文件名',
    `file_path` VARCHAR(500) NOT NULL COMMENT '文件存储路径',
    `file_size` BIGINT DEFAULT 0 COMMENT '文件大小（字节）',
    `file_type` VARCHAR(50) COMMENT '文件类型（pdf/docx/txt等）',
    `status` TINYINT NOT NULL DEFAULT 0 COMMENT '状态：0待处理 1处理中 2成功 3失败',
    `task_id` VARCHAR(64) COMMENT '异步任务ID',
    `chunk_count` INT DEFAULT 0 COMMENT '切片数量',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `is_deleted` TINYINT NOT NULL DEFAULT 0 COMMENT '逻辑删除：0未删 1已删',
    PRIMARY KEY (`id`),
    KEY `idx_tenant_status` (`tenant_id`, `status`),
    KEY `idx_task_id` (`task_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文档表';

-- 对话会话表
CREATE TABLE IF NOT EXISTS `biz_conversation` (
    `id` BIGINT NOT NULL COMMENT '会话ID',
    `tenant_id` BIGINT NOT NULL COMMENT '租户ID',
    `title` VARCHAR(255) COMMENT '会话标题',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `is_deleted` TINYINT NOT NULL DEFAULT 0 COMMENT '逻辑删除：0未删 1已删',
    PRIMARY KEY (`id`),
    KEY `idx_tenant_create` (`tenant_id`, `create_time`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='对话会话表';

-- 消息表
CREATE TABLE IF NOT EXISTS `biz_message` (
    `id` BIGINT NOT NULL COMMENT '消息ID',
    `tenant_id` BIGINT NOT NULL COMMENT '租户ID',
    `conversation_id` BIGINT NOT NULL COMMENT '所属会话ID',
    `role` VARCHAR(20) NOT NULL COMMENT '角色：user/assistant/system',
    `content` TEXT NOT NULL COMMENT '消息内容',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `is_deleted` TINYINT NOT NULL DEFAULT 0 COMMENT '逻辑删除：0未删 1已删',
    PRIMARY KEY (`id`),
    KEY `idx_conversation_create` (`conversation_id`, `create_time`),
    KEY `idx_tenant` (`tenant_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='消息表';

-- 异步任务表
CREATE TABLE IF NOT EXISTS `sys_task` (
    `id` BIGINT NOT NULL COMMENT '任务ID',
    `task_type` VARCHAR(50) NOT NULL COMMENT '任务类型（如：document_process）',
    `status` VARCHAR(20) NOT NULL DEFAULT 'PENDING' COMMENT '任务状态：PENDING/PROCESSING/SUCCESS/FAILED',
    `progress` INT DEFAULT 0 COMMENT '进度（0-100）',
    `error_msg` TEXT COMMENT '错误信息',
    `result` TEXT COMMENT '任务结果（JSON）',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_status` (`status`),
    KEY `idx_type_status` (`task_type`, `status`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='异步任务表';
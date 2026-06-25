-- 扩展 biz_document 表，增加大模型解析和审计相关字段

-- 1. 新增业务字段
ALTER TABLE `biz_document`
    ADD COLUMN `category_id` BIGINT DEFAULT NULL COMMENT '文档分类ID' AFTER `tenant_id`,
    ADD COLUMN `remark` VARCHAR(500) DEFAULT NULL COMMENT '文档备注说明' AFTER `category_id`,
    ADD COLUMN `is_public` TINYINT DEFAULT 0 COMMENT '是否公开：0-私有，1-公开' AFTER `remark`;

-- 2. 新增文件元信息字段（细化）
ALTER TABLE `biz_document`
    ADD COLUMN `original_file_name` VARCHAR(255) NOT NULL COMMENT '原始文件名称' AFTER `is_public`,
    ADD COLUMN `storage_file_name` VARCHAR(255) NOT NULL COMMENT '文件存储唯一名称' AFTER `original_file_name`,
    ADD COLUMN `file_url` VARCHAR(500) NOT NULL COMMENT '文件存储完整访问路径' AFTER `storage_file_name`,
    ADD COLUMN `mime_type` VARCHAR(100) DEFAULT NULL COMMENT '文件MIME类型' AFTER `file_url`,
    ADD COLUMN `file_suffix` VARCHAR(20) DEFAULT NULL COMMENT '文件后缀' AFTER `mime_type`;

-- 3. 新增操作人审计字段
ALTER TABLE `biz_document`
    ADD COLUMN `create_user_id` BIGINT DEFAULT NULL COMMENT '上传人用户ID' AFTER `file_suffix`,
    ADD COLUMN `create_user_name` VARCHAR(100) DEFAULT NULL COMMENT '上传人账号名称' AFTER `create_user_id`,
    ADD COLUMN `update_user_id` BIGINT DEFAULT NULL COMMENT '更新人ID' AFTER `create_user_name`;

-- 4. 新增大模型解析 RAG 字段
ALTER TABLE `biz_document`
    ADD COLUMN `doc_content` LONGTEXT COMMENT '文档纯文本内容（提取后给大模型解析）' AFTER `update_user_id`,
    ADD COLUMN `doc_summary` VARCHAR(1000) DEFAULT NULL COMMENT '大模型提取的文档摘要' AFTER `doc_content`,
    ADD COLUMN `vector_id` VARCHAR(64) DEFAULT NULL COMMENT '向量库唯一ID（Milvus）' AFTER `doc_summary`,
    ADD COLUMN `parse_status` TINYINT DEFAULT 0 COMMENT '解析状态：0-待解析 1-成功 2-失败' AFTER `vector_id`,
    ADD COLUMN `parse_error_msg` TEXT DEFAULT NULL COMMENT '解析失败原因' AFTER `parse_status`;

-- 5. 新增索引（优化查询性能）
ALTER TABLE `biz_document`
    ADD INDEX `idx_parse_status` (`parse_status`),
    ADD INDEX `idx_category_id` (`category_id`),
    ADD INDEX `idx_original_file_name` (`original_file_name`(50));
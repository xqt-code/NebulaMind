package com.nebulamind.kb.dao.entity;

import com.baomidou.mybatisplus.annotation.TableName;
import com.nebulamind.kb.common.entity.BaseEntity;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * 文档实体类。
 *
 * 对应数据库表：biz_document
 * 职责：存储典则文档的元数据 + 异步解析状态追踪。
 *
 * 字段与数据库列映射关系：
 *   - 驼峰命名自动转下划线（如 originalFileName → original_file_name）
 *
 * 核心设计：
 *   1. 文件元数据字段：记录上传时的文件信息，用于展示和下载。
 *   2. 解析状态字段：支持前端轮询查询解析进度。
 *   3. 继承 BaseEntity：自动获得 id、tenantId、审计时间、逻辑删除。
 *
 * @author NebulaMind
 */
@Data
@EqualsAndHashCode(callSuper = true)
@TableName("biz_document")
@Schema(description = "电力典则文档实体")
public class Document extends BaseEntity {

    // ================================================================
    // 一、文件元信息（上传时由 Service 层填充）
    // ================================================================

    @Schema(description = "原始文件名称（用户上传时的文件名）", example = "典则2018_10kV架空线路.pdf")
    private String originalFileName;

    @Schema(description = "文件存储唯一名称（UUID 生成，防止重名覆盖）", example = "a1b2c3d4-e5f6-7890-abcd-ef1234567890.pdf")
    private String storageFileName;

    @Schema(description = "文件访问完整路径（MinIO 或本地存储的 URL）", example = "http://localhost:9000/bucket/a1b2c3d4.pdf")
    private String fileUrl;

    @Schema(description = "文件大小（字节）", example = "15728640")
    private Long fileSize;

    @Schema(description = "文件 MIME 类型", example = "application/pdf")
    private String mimeType;

    @Schema(description = "文件后缀（小写）", example = "pdf")
    private String fileSuffix;

    // ================================================================
    // 二、异步解析状态追踪（前端轮询依赖的核心字段）
    // ================================================================

    @Schema(description = "解析状态: PENDING（待处理）| PARSING（解析中）| PARSED（解析完成）| FAILED（解析失败）",
            example = "PARSING", allowableValues = {"PENDING", "PARSING", "PARSED", "FAILED"})
    private String parseStatus;

    @Schema(description = "解析进度（0-100），前端用于展示进度条", example = "65")
    private Integer parseProgress;

    @Schema(description = "解析结果 JSON（存典则表格、规则等结构化数据）")
    private String parseResult;

    @Schema(description = "解析失败时的错误信息（便于排查问题）", example = "PDF 表格格式异常，无法抽取")
    private String errorMessage;

    // ================================================================
    // 三、保留旧业务字段（用 @TableField(exist = false) 忽略）
    //    不映射到数据库，但保留在代码中供未来扩展使用。
    //    exist = false 表示 MyBatis-Plus 在增删改查时忽略这些字段。
    // ================================================================

    // @TableField(exist = false)
    // private Long categoryId;          // 文档分类 ID（未来用于按专业分类）

    // @TableField(exist = false)
    // private String remark;            // 文档备注

    // @TableField(exist = false)
    // private Integer isPublic;         // 是否公开（未来用于多租户共享）

    // @TableField(exist = false)
    // private String docContent;        // 文档纯文本（RAG 解析后的内容）

    // @TableField(exist = false)
    // private String docSummary;        // 文档摘要（大模型生成）

    // @TableField(exist = false)
    // private String vectorId;          // 向量库 ID（对接 Milvus 时使用）

    // @TableField(exist = false)
    // private Long createUserId;        // 上传人 ID（将来接用户系统时启用）

    // @TableField(exist = false)
    // private String createUserName;    // 上传人名称（将来接用户系统时启用）

    // @TableField(exist = false)
    // private Long updateUserId;        // 更新人 ID（将来接用户系统时启用）
}
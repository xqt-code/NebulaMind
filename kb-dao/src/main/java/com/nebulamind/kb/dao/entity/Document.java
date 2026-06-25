package com.nebulamind.kb.dao.entity;

import com.baomidou.mybatisplus.annotation.FieldFill;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableName;
import com.nebulamind.kb.common.entity.BaseEntity;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * 文档实体类。
 * 对应数据库表 biz_document，用于存储上传的文档信息。
 *
 * @author NebulaMind
 */
/**
 * 文档实体类（员工知识库文档存储）
 */
@Data
@EqualsAndHashCode(callSuper = true)
@TableName("biz_document")
@Schema(description = "员工知识库文档存储实体")
public class Document extends BaseEntity {

    // ========== 前端传入字段（来自 DocumentUploadRequest） ==========

    @Schema(description = "文档分类ID")
    private Long categoryId;

    @Schema(description = "文档备注说明")
    private String remark;

    @Schema(description = "是否公开：0-私有，1-公开")
    private Integer isPublic;


    // ========== 文件元信息（后端解析 MultipartFile 自动填充） ==========

    @Schema(description = "原始文件名称（员工上传的文件名）")
    private String originalFileName;

    @Schema(description = "文件存储唯一名称（MinIO/OSS 文件名，防止重名覆盖）")
    private String storageFileName;

    @Schema(description = "文件存储完整访问路径")
    private String fileUrl;

    @Schema(description = "文件大小（字节）")
    private Long fileSize;

    @Schema(description = "文件MIME类型：application/pdf、application/msword等")
    private String mimeType;

    @Schema(description = "文件后缀：pdf/docx/txt/xlsx")
    private String fileSuffix;


    // ========== 操作溯源字段（自动填充） ==========

    @Schema(description = "上传人用户ID")
    @TableField(fill = FieldFill.INSERT)
    private Long createUserId;

    @Schema(description = "上传人账号名称")
    @TableField(fill = FieldFill.INSERT)
    private String createUserName;

    @Schema(description = "更新人ID")
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private Long updateUserId;


    // ========== 大模型解析 RAG 业务专属字段 ==========

    @Schema(description = "文档纯文本内容（提取后给大模型解析使用）")
    private String docContent;

    @Schema(description = "大模型提取的文档摘要（前端展示预览）")
    private String docSummary;

    @Schema(description = "向量库唯一ID（Milvus 主键，检索用）")
    private String vectorId;

    @Schema(description = "文档解析状态：0-待解析，1-解析成功，2-解析失败")
    private Integer parseStatus;

    @Schema(description = "解析失败原因（用于排查大模型读取文档报错）")
    private String parseErrorMsg;
}
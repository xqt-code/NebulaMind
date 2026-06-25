package com.nebulamind.kb.service.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import org.springframework.web.multipart.MultipartFile;

/**
 * 文档上传请求 DTO。
 * 用于接收前端上传文档时的请求参数。
 *
 * @author NebulaMind
 */
@Data
@Schema(description = "文档上传入参实体")
public class DocumentUploadRequest {

    // ========== 前端传入字段（来自 DocumentUploadRequest） ==========
    /**
     * 待上传的文件
     * 必传，支持PDF/Word/TXT/Excel等文档类型，后端统一校验文件大小、后缀、文件MIME类型
     */
    @NotNull(message = "上传文件不能为空")
    @Schema(description = "待上传文档文件", requiredMode = Schema.RequiredMode.REQUIRED)
    private MultipartFile file;

    /**
     * 文档分类ID
     * 用于对文档做业务分类管理，非必传，不传则归为默认未分类分组
     */
    @Schema(description = "文档分类ID", requiredMode = Schema.RequiredMode.NOT_REQUIRED)
    private Long categoryId;

    /**
     * 文档自定义备注描述
     * 用户填写的文档说明、备注信息，用于前端展示
     */
    @Schema(description = "文档备注说明", requiredMode = Schema.RequiredMode.NOT_REQUIRED)
    private String remark;

    /**
     * 文档公开标识
     * 0：私有文档，仅本人与租户管理员可见
     * 1：公开文档，租户内所有用户均可查看
     */
    @Schema(description = "是否公开 0私有 1公开，默认0", requiredMode = Schema.RequiredMode.NOT_REQUIRED)
    private Integer isPublic;
}
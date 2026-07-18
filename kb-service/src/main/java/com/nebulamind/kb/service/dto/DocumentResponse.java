package com.nebulamind.kb.service.dto;

import io.swagger.v3.oas.annotations.media.Schema;

/**
 * 文档详情响应 DTO（Data Transfer Object）。
 *
 * 职责：作为 Controller 层返回给前端的数据契约（Contract）。
 * 为什么不用 Entity（数据库实体）直接返回？
 *   1. 安全性：Entity 包含 storageFileName（存储路径）、tenantId（租户ID）等内部敏感字段，不应暴露给前端。
 *   2. 解耦：数据库表结构变更（如改名），只要 DTO 不变，前端就无需改动。
 *   3. 灵活性：可以组合多张表的数据，或对字段进行格式化（如日期转字符串）。
 *
 * @author NebulaMind
 */
@Schema(description = "文档详情响应对象")
public class DocumentResponse {

    @Schema(description = "文档主键 ID", example = "1001")
    private Long id;

    @Schema(description = "文件原始名称", example = "典则2018_10kV架空线路.pdf")
    private String originalFileName;

    @Schema(description = "文件大小（字节）", example = "15728640")
    private Long fileSize;

    @Schema(description = "文件访问 URL", example = "http://minio:9000/bucket/xxx.pdf")
    private String fileUrl;

    // ==================== 异步任务状态追踪字段 ====================

    @Schema(description = "解析状态: PENDING(待处理) | PARSING(解析中) | PARSED(解析完成) | FAILED(解析失败)",
            example = "PARSING",
            allowableValues = {"PENDING", "PARSING", "PARSED", "FAILED"})
    private String parseStatus;

    @Schema(description = "解析进度 (0-100)", example = "65")
    private Integer parseProgress;

    @Schema(description = "解析失败时的错误信息", example = "PDF 表格格式异常，无法抽取")
    private String errorMessage;

    @Schema(description = "解析成功后，返回的典则结构化数据 JSON（此字段较大，前端仅在解析完成后按需拉取）")
    private String parseResult;

    // ==================== Getter & Setter ====================
    // 企业级规范要求：Lombok 可以简化，但如果你不用 Lombok，手写 getter/setter 是必须的。
    // 为了让你看清全貌，我手写标准模板。

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getOriginalFileName() { return originalFileName; }
    public void setOriginalFileName(String originalFileName) { this.originalFileName = originalFileName; }

    public Long getFileSize() { return fileSize; }
    public void setFileSize(Long fileSize) { this.fileSize = fileSize; }

    public String getFileUrl() { return fileUrl; }
    public void setFileUrl(String fileUrl) { this.fileUrl = fileUrl; }

    public String getParseStatus() { return parseStatus; }
    public void setParseStatus(String parseStatus) { this.parseStatus = parseStatus; }

    public Integer getParseProgress() { return parseProgress; }
    public void setParseProgress(Integer parseProgress) { this.parseProgress = parseProgress; }

    public String getErrorMessage() { return errorMessage; }
    public void setErrorMessage(String errorMessage) { this.errorMessage = errorMessage; }

    public String getParseResult() { return parseResult; }
    public void setParseResult(String parseResult) { this.parseResult = parseResult; }
}
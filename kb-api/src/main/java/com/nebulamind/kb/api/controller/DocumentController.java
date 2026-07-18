package com.nebulamind.kb.api.controller;

import com.nebulamind.kb.common.result.Result;
import com.nebulamind.kb.common.result.ResultCode;
import com.nebulamind.kb.service.dto.DocumentResponse;
import com.nebulamind.kb.service.dto.DocumentUploadRequest;
import com.nebulamind.kb.service.service.DocumentService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

/**
 * 文档管理控制器。
 * 提供文档上传、查询、删除等 REST API 接口。
 *
 * @author NebulaMind
 */
@Tag(name = "文档管理", description = "文档上传、查询、删除接口")
@RestController
@RequestMapping("/api/v1/documents")
public class DocumentController {

    @Autowired
    DocumentService documentService;

    /**
     * 上传文档。
     * 接收用户上传的文件，异步处理文档解析和入库。
     *
     * @param file     上传的文件
     * @param tenantId 租户 ID（可选）
     * @return 任务 ID
     */
    @Operation(summary = "上传文档")
    @PostMapping("/upload")

    public Result<String> upload(@Valid @ModelAttribute DocumentUploadRequest dto) {
        // TODO: 实现文档上传逻辑，异步处理文档解析
        Long documentID = documentService.uploadDocument(dto);
        return Result.success(documentID+"");
    }

    /**
     * 获取文档列表。
     * 分页查询文档列表，支持关键字搜索。
     *
     * @param page    页码，默认 1
     * @param size    每页条数，默认 10
     * @param keyword 搜索关键字（可选）
     * @return 文档列表
     */
    @Operation(summary = "获取文档列表")
    @GetMapping("/list")
    public Result<Void> list(
            @Parameter(description = "页码") @RequestParam(defaultValue = "1") Integer page,
            @Parameter(description = "每页条数") @RequestParam(defaultValue = "10") Integer size,
            @Parameter(description = "搜索关键字") @RequestParam(required = false) String keyword) {
        // TODO: 实现文档分页查询逻辑
        return Result.success(null);
    }

    /**
     * 获取文档详情。
     *
     * @param id 文档 ID
     * @return 文档详情
     */
    @Operation(summary = "获取文档详情")
    @GetMapping("/{id}")
    public Result<DocumentResponse> detail(
            @Parameter(description = "文档 ID", required = true) @PathVariable Long id) {
        // TODO: 实现文档详情查询逻辑
        DocumentResponse response = documentService.getDocumentDetail(id);
        return Result.success(response);
    }

    /**
     * 删除文档。
     *
     * @param id 文档 ID
     * @return 操作结果
     */
    @Operation(summary = "删除文档")
    @DeleteMapping("/{id}")
    public Result<String> delete(
            @Parameter(description = "文档 ID", required = true) @PathVariable Long id) {
        // TODO: 实现文档删除逻辑
        return Result.success("删除成功");
    }
}
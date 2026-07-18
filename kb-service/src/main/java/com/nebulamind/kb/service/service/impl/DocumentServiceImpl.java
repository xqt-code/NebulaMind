package com.nebulamind.kb.service.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.nebulamind.kb.common.exception.BusinessException;
import com.nebulamind.kb.common.result.PageResult;
import com.nebulamind.kb.common.result.ResultCode;
import com.nebulamind.kb.dao.entity.Document;
import com.nebulamind.kb.dao.mapper.DocumentMapper;
import com.nebulamind.kb.service.convert.DocumentConvert;
import com.nebulamind.kb.service.dto.DocumentResponse;
import com.nebulamind.kb.service.dto.DocumentUploadRequest;
import com.nebulamind.kb.service.service.DocumentService;
import io.minio.*;
import io.minio.errors.ErrorResponseException;
import io.minio.errors.MinioException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;
import lombok.extern.slf4j.Slf4j;  // ← 这是注解

import java.io.IOException;
import java.util.UUID;
import java.util.concurrent.TimeUnit;

import static com.nebulamind.kb.common.util.FileUtil.getFileExtension;

/**
 * 文档服务实现类。
 * 提供文档相关的业务逻辑实现。
 *
 * @author NebulaMind
 */
@Service
@Slf4j
public class DocumentServiceImpl extends ServiceImpl<DocumentMapper, Document> implements DocumentService {
    // 上传文档，保存文件信息到数据库
    @Autowired
    private DocumentConvert documentConvert;

    @Autowired
    private MinioClient minioClient;

    // 从配置读取桶名
    @Value("${minio.bucket}")
    private String bucket;

    // 从配置读取桶IP
    @Value("${minio.endpoint}")
    private String endpoint;

    @Override
    @Transactional(rollbackFor = Exception.class)
    public Long uploadDocument(DocumentUploadRequest documentUploadRequest) {
        // ====== 1. 获取上传文件 ======
        MultipartFile multipartFile = documentUploadRequest.getFile();

        if (multipartFile == null || multipartFile.isEmpty()) {
            throw new BusinessException(ResultCode.BAD_REQUEST.getCode(), "文件不能为空");
        }

        String originalFileName = multipartFile.getOriginalFilename();
        String ext = getFileExtension(originalFileName);
        String storageFileName = UUID.randomUUID() + "_" + System.currentTimeMillis() + ext;
        String fileUrl = endpoint + "/" + bucket + "/" + storageFileName;

        // ====== 2. 创建实体并填充字段（此时还没有 ID，插入后由 MP 自动生成） ======
        Document document = documentConvert.toEntity(documentUploadRequest);

        document.setOriginalFileName(originalFileName);
        document.setStorageFileName(storageFileName);
        document.setFileUrl(fileUrl);
        document.setFileSize(multipartFile.getSize());
        document.setMimeType(multipartFile.getContentType());
        document.setFileSuffix(ext);
        // 注意：BaseEntity 里的 tenantId 在 BaseEntity 基类里已有，直接设置
        document.setTenantId(1L);  // 单租户固定为 1

        // parseStatus 和 parseProgress 不设置，数据库有默认值（PENDING 和 0）

        // ====== 3. 上传到 MinIO（或本地存储） ======
        try {
            // 检查是否已存在同名文件
            try {
                minioClient.statObject(
                        StatObjectArgs.builder()
                                .bucket(bucket)
                                .object(storageFileName)
                                .build()
                );
                // 存在则删除
                minioClient.removeObject(
                        RemoveObjectArgs.builder()
                                .bucket(bucket)
                                .object(storageFileName)
                                .build()
                );
            } catch (ErrorResponseException e) {
                // 文件不存在 → 忽略，继续上传
                if (!"NoSuchKey".equals(e.errorResponse().code())) {
                    log.error("MinIO 检查文件异常，错误码：{}", e.errorResponse().code(), e);
                    throw new BusinessException(ResultCode.INTERNAL_ERROR.getCode(), "文件存储服务异常");
                }
            }

            // 上传文件
            minioClient.putObject(
                    PutObjectArgs.builder()
                            .bucket(bucket)
                            .object(storageFileName)
                            .stream(multipartFile.getInputStream(), multipartFile.getSize(), -1)
                            .contentType(multipartFile.getContentType())
                            .build()
            );

        } catch (MinioException e) {
            log.error("MinIO 上传失败，文件：{}，错误：{}", originalFileName, e.getMessage(), e);
            throw new BusinessException(ResultCode.INTERNAL_ERROR.getCode(), "文件上传失败，请重新上传");
        } catch (IOException e) {
            log.error("文件读取失败，文件：{}，错误：{}", originalFileName, e.getMessage(), e);
            throw new BusinessException(ResultCode.INTERNAL_ERROR.getCode(), "文件读取失败，请重新上传");
        } catch (Exception e) {
            log.error("文档上传异常，文件：{}，错误：{}", originalFileName, e.getMessage(), e);
            throw new BusinessException(ResultCode.INTERNAL_ERROR.getCode(), "文档上传失败，请稍后重试");
        }

        // ====== 4. 插入数据库 ======
        Long tenantId = 1L;

        // 检查是否已存在同名文件（防止重复上传）
        LambdaQueryWrapper<Document> queryWrapper = new LambdaQueryWrapper<>();
        queryWrapper.eq(Document::getOriginalFileName, originalFileName)
                .eq(Document::getTenantId, tenantId)
                .eq(Document::getIsDeleted, 0);  // 只查未删除的记录

        Document oldDoc = this.getOne(queryWrapper);

        if (oldDoc == null) {
            // 不存在 → 新增
            boolean result = this.save(document);
            if (!result) {
                throw new BusinessException(ResultCode.BAD_REQUEST, "文档保存失败");
            }
            log.info("文档上传成功（新增）：originalFileName={}, id={}", originalFileName, document.getId());
            return document.getId();
        } else {
            // 已存在 → 更新（只更新文件相关的字段，不覆盖其他字段）
            oldDoc.setOriginalFileName(originalFileName);
            oldDoc.setStorageFileName(storageFileName);
            oldDoc.setFileUrl(fileUrl);
            oldDoc.setFileSize(multipartFile.getSize());
            oldDoc.setMimeType(multipartFile.getContentType());
            oldDoc.setFileSuffix(ext);
            // 注意：不要动 parseStatus、parseProgress、parseResult，因为已有的解析记录应该保留

            boolean result = this.updateById(oldDoc);
            if (!result) {
                throw new BusinessException(ResultCode.BAD_REQUEST, "文档更新失败");
            }
            log.info("文档上传成功（覆盖更新）：originalFileName={}, id={}", originalFileName, oldDoc.getId());
            return oldDoc.getId();
        }
    }

    // DocumentServiceImpl 实现
    @Override
    public String getFileUrl(Long documentId) {
        Document doc = this.getById(documentId);
        if (doc == null) {
            throw new BusinessException(ResultCode.NOT_FOUND.getCode(), "文档不存在");
        }
        try {
            return minioClient.getPresignedObjectUrl(
                    GetPresignedObjectUrlArgs.builder()
                            .bucket(bucket)
                            .object(doc.getStorageFileName())
                            .expiry(7, TimeUnit.DAYS)
                            .build()
            );
        } catch (Exception e) {
            log.error("生成文档访问链接失败，文档ID：{}", documentId, e);
            throw new BusinessException(ResultCode.INTERNAL_ERROR.getCode(), "获取文件链接失败");
        }
    }

    // 分页查询文档列表
    @Override
    public PageResult<DocumentResponse> listDocuments(int page, int size, String keyword) {
        return null;
    }

    // ======================================================================
    // 业务方法实现：查询文档详情
    // ======================================================================

    /**
     * {@inheritDoc}
     *
     * 实现细节：
     * 1. 通过 MyBatis-Plus 的 getById 查询数据库。
     * 2. 若查不到，抛出 BusinessException（由全局异常处理器统一返回 404）。
     * 3. 若查到，通过 MapStruct 转换为 DTO。
     * 4. 补充状态字段（解析状态），用于前端轮询。
     */
    @Override
    public DocumentResponse getDocumentDetail(Long id) {
        // ====== 1. 日志记录（入参） ======
        // 企业级要求：必须记录关键入参，便于排查“谁查了什么”。
        log.info("开始查询文档详情，documentId = {}", id);

        // ====== 2. 参数校验（防御性编程） ======
        // 虽然 Controller 层 @PathVariable 会校验，但 Service 层仍要防御。
        // 这是企业级规范：不信任任何调用方（包括 Controller）。
        if (id == null || id <= 0) {
            log.warn("查询文档详情失败，ID 非法：id = {}", id);
            throw new BusinessException(ResultCode.BAD_REQUEST, "文档 ID 不能为空或小于 0");
        }

        // ====== 3. 执行数据库查询 ======
        // 调用 MyBatis-Plus 基类方法：根据主键 ID 查询单条记录。
        // 等价于执行 SQL: SELECT * FROM biz_document WHERE id = ? AND deleted = 0（逻辑删除）
        Document document = this.getById(id);

        // ====== 4. 判断是否存在（业务逻辑） ======
        if (document == null) {
            // 日志记录（错误级别）：记录查不到的情况
            log.error("文档不存在，documentId = {}", id);
            // 抛出业务异常，由 @ControllerAdvice 统一处理，返回前端 404 JSON
            throw new BusinessException(ResultCode.NOT_FOUND, "文档不存在");
        }

        // ====== 5. 日志记录（查询成功） ======
        log.info("文档查询成功，documentId = {}, fileName = {}", id, document.getOriginalFileName());

        // ====== 6. 对象转换（Entity -> DTO） ======
        // 使用 MapStruct 转换器，避免大量手写 setter 代码。
        // 如果 MapStruct 未配置，这里会报空指针，请确保 DocumentConvert 有 @Mapper(componentModel = "spring")。
        DocumentResponse response = documentConvert.toResponse(document);

        // ====== 7. 补充前端需要的额外状态（拓展逻辑） ======
        // 说明：当前数据库表中可能还没有 parseStatus 字段（因为还没用 DDL 添加），
        // 此处直接设置默认值，保证接口立即可用（前端不报错）。
        // 注：若数据库已有该字段，MapStruct 会根据名称自动映射，这里加一层判断防止覆盖。
        if (response.getParseStatus() == null) {
            // 默认置为 PENDING（待处理），等后续 FastAPI 回调时更新。
            response.setParseStatus("PENDING");
            response.setParseProgress(0);
        }

        // ====== 8. 返回结果 ======
        log.info("文档详情查询完成，返回结果：id = {}, status = {}",
                response.getId(), response.getParseStatus());
        return response;
    }

    // 逻辑删除文档
    @Override
    public void deleteDocument(Long id) {

    }
}
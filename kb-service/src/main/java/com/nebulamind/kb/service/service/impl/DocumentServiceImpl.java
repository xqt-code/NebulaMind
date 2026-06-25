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
//        校验 dto.file 文件合法性；
//        校验传入 tenantId 权限，无则使用登录上下文租户；
//        文件上传 MinIO，生成 minio 文件访问地址；
//        MapStruct 将 DocUploadDTO 转换为 Document 数据库实体；
//        后端手动填充 minioUrl、fileSize、suffix、tenantId；
//        MP 自动填充创建人、创建时间，插入数据库；
//        异步调用 FastAPI，传递 documentId 与 minioUrl 执行 LangChain 文档标注。

        // 要处理的文档
        MultipartFile multipartFile = documentUploadRequest.getFile();

        if (multipartFile == null || multipartFile.isEmpty()) {
            throw new BusinessException(ResultCode.BAD_REQUEST.getCode(), "文件不能为空");
        }

        String originalFileName = multipartFile.getOriginalFilename();
        String ext = getFileExtension(originalFileName);
        String storageFileName = UUID.randomUUID() + "_" + System.currentTimeMillis() + ext;
        String fileUrl = endpoint + "/" + bucket + "/" + storageFileName;

        Document document = documentConvert.toEntity(documentUploadRequest);

        document.setOriginalFileName(originalFileName);
        document.setStorageFileName(storageFileName);
        document.setFileUrl(fileUrl);
        document.setFileSize(multipartFile.getSize());
        document.setMimeType(multipartFile.getContentType());
        document.setFileSuffix(ext);

        // 检查MinIO里存不存在这个文件
        try{
            // 检查文件是否已存在
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
        }catch (ErrorResponseException e) {
            // 文件不存在 → 忽略，继续上传
            if (!"NoSuchKey".equals(e.errorResponse().code())) {
                log.error("MinIO 检查文件异常，错误码：{}", e.errorResponse().code(), e);
                throw new BusinessException(ResultCode.INTERNAL_ERROR.getCode(), "文件存储服务异常");
            }
        } catch (MinioException e){
            log.error("MinIO 上传失败，文件：{}，错误：{}", originalFileName, e.getMessage(), e);
            throw new BusinessException(ResultCode.INTERNAL_ERROR.getCode(), "文件读取失败，请重新上传");
        }catch (IOException e) {
            log.error("文件读取失败，文件：{}，错误：{}", originalFileName, e.getMessage(), e);
            throw new BusinessException(ResultCode.INTERNAL_ERROR.getCode(), "文件读取失败，请重新上传");
        }catch (Exception e) {
            log.error("文档上传异常，文件：{}，错误：{}", originalFileName, e.getMessage(), e);
            throw new BusinessException(ResultCode.INTERNAL_ERROR.getCode(), "文档上传失败，请稍后重试");
        }

        try{
            // 上传到 MinIO
            minioClient.putObject(
                    PutObjectArgs.builder()
                            .bucket(bucket)
                            .object(storageFileName)
                            .stream(multipartFile.getInputStream(), multipartFile.getSize(), -1)
                            .contentType(multipartFile.getContentType())
                            .build()
            );

        }catch (MinioException e){
            log.error("MinIO 上传失败，文件：{}，错误：{}", originalFileName, e.getMessage(), e);
            throw new BusinessException(ResultCode.INTERNAL_ERROR.getCode(), "文件读取失败，请重新上传");
        }catch (IOException e) {
            log.error("文件读取失败，文件：{}，错误：{}", originalFileName, e.getMessage(), e);
            throw new BusinessException(ResultCode.INTERNAL_ERROR.getCode(), "文件读取失败，请重新上传");
        }catch (Exception e) {
            log.error("文档上传异常，文件：{}，错误：{}", originalFileName, e.getMessage(), e);
            throw new BusinessException(ResultCode.INTERNAL_ERROR.getCode(), "文档上传失败，请稍后重试");
        }

        // 插入数据库
        Long tenantId = 1L;

        LambdaQueryWrapper<Document> queryWrapper = new LambdaQueryWrapper<Document>();
        queryWrapper.eq(Document::getOriginalFileName, originalFileName );
        queryWrapper.eq(Document::getTenantId, tenantId);

        Document oldDoc = this.getOne(queryWrapper);

        // 数据库不存在这个文件
        if (oldDoc == null) {
            Boolean result = this.save(document);
            if (!result) {
                throw new BusinessException(ResultCode.BAD_REQUEST);
            }

            log.info("文档上传成功：originalFileName={}, storageFileName={}", originalFileName, storageFileName);
            return document.getId();
        }else{
            oldDoc.setCategoryId(document.getCategoryId());
            oldDoc.setRemark(document.getRemark());
            oldDoc.setIsPublic(document.getIsPublic());
            oldDoc.setOriginalFileName(originalFileName);
            oldDoc.setStorageFileName(storageFileName);
            oldDoc.setFileUrl(fileUrl);
            oldDoc.setFileSize(document.getFileSize());
            oldDoc.setMimeType(document.getMimeType());
            oldDoc.setFileSuffix(document.getFileSuffix());

            // 数据库存在这个文件,覆盖更新
            Boolean result = this.updateById(oldDoc);
            if (!result) {
                throw new BusinessException(ResultCode.BAD_REQUEST);
            }
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

    // 查询文档详情
    @Override
    public DocumentResponse getDocumentDetail(Long id) {
        return null;
    }

    // 逻辑删除文档
    @Override
    public void deleteDocument(Long id) {

    }
}
package com.nebulamind.kb.service.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.nebulamind.kb.common.result.PageResult;
import com.nebulamind.kb.dao.entity.Document;
import com.nebulamind.kb.service.dto.DocumentResponse;
import com.nebulamind.kb.service.dto.DocumentUploadRequest;

/**
 * 文档服务接口。
 * 定义文档上传、查询、删除等业务操作。
 *
 * @author NebulaMind
 */
public interface DocumentService extends IService<Document> {

    // TODO: 定义文档相关业务方法
    // 上传文档，保存文件信息到数据库
    Long uploadDocument(DocumentUploadRequest documentUploadRequest);

    // 根据ID获取minio文档路径
    String getFileUrl(Long documentId);

    // 分页查询文档列表
    PageResult<DocumentResponse> listDocuments(int page, int size, String keyword);

    // 查询文档详情
    DocumentResponse getDocumentDetail(Long id);

    // 逻辑删除文档
    void deleteDocument(Long id);

}